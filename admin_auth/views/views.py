from django.shortcuts import get_object_or_404
from django.shortcuts import render
from ..global_func import checkUserExist
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from ..models import Produce, Vegetable, CartItem, UserProfile
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            # Check user role
            if user.is_superuser:
                return redirect('admin-dashboard')
            else:
              return redirect('farmer-dashboard')
        else:
             # Check for inactive user to show proper error
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                check_user = User.objects.get(username=username)
                if not check_user.is_active:
                    error = 'Account is inactive. Please contact the administrator.'
                else:
                    error = 'Invalid username or password.'
            except User.DoesNotExist:
                error = 'Invalid username or password.'

            return render(request, 'login.html', {'error': error})
        
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('farmer-dashboard')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

@csrf_exempt
def register_view(request):
    json_error = []
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            json_error.append('Username is required')
        password = request.POST.get('password')
        if not password:
            json_error.append('password is required')
        password2 = request.POST.get('password2')
        if not password2:
            json_error.append('Retype password is required')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        if not phone_number:
            json_error.append('Phone Number is required')
        
        if password != password2:
           json_error.append("Passwords do not match.")
        
        if User.objects.filter(username=username).exists():
            json_error.append("Username already exists.")
        
        if json_error:
            return JsonResponse({'error': json_error}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email, phone_number=phone_number)
        # login(request, user)  # Auto-login after registration
        return redirect('login')  # Redirect to homepage after registration

    return render(request, 'logisteration.html')


def index(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'index.html', context) 

@login_required(login_url='login')
def admin_dashboard(request):
    users = User.objects.all() 
    produce_list = Produce.objects.all()
    context = {
        'produce_list': produce_list,
        'users': users
    }
    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='login')
def farmer_dashboard(request):
    produce_list  = Produce.objects.filter(created_by=request.user, status="approved").all()
    vegetables = Vegetable.objects.all()
    context = {
        'produce_list': produce_list,
        'vegetables': vegetables,
        'user': f'{request.user.username}'
    }
    return render(request, 'farmer/dashboard.html', context)

from django.core.mail import send_mail
from django.conf import settings

@require_POST
def change_produce_status(request, pk):
    produce = get_object_or_404(Produce, pk=pk)

    # Optional: add permission check
    # if not request.user.is_staff: return HttpResponseForbidden()

    new_status = request.POST.get('status')
    if new_status in ['approved', 'rejected']:
        produce.status = new_status
        produce.save()
         # Send email notification
        subject = f"Produce Status Changed to {new_status.capitalize()}"
        message = f"The status of the produce item '{produce.name}' has been changed to '{new_status}'."
        recipient_email = "bhimpdraj123@gmail.com"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # From email
            [recipient_email],  # To email
            fail_silently=False,
        )

    return redirect('admin-dashboard')  # change this to your list view name


def toggle_user_status(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)

        # Prevent modifying superusers
        if not user.is_superuser:
            user.is_active = not user.is_active
            user.save()

    return redirect(request.POST.get('next', 'admin-dashboard'))

def certification(request):
    return render(request, 'certification.html')


def consumer(request):
    context = {
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'consumer.html', context)

def get_consumer_data(request):
    produce_list = Produce.objects.filter(status='approved').select_related('name')

    # Serialize data to JSON
    data = list(produce_list.values(
        'id',
        'name__name',     # name is a ForeignKey to Vegetable
        'quantity',
        'price',
        'certification',
        'remarks',
        'status',
        'created_by_id'
    ))

    return JsonResponse(data, safe=False)


@login_required(login_url='login')
def cart(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        bank_qr_url = profile.bank_qr.url if profile.bank_qr else None
    except UserProfile.DoesNotExist:
        bank_qr_url = None

    return render(request, 'cart.html', {'bank_qr_url': bank_qr_url})


import json
@csrf_exempt  # or use CSRF token in AJAX instead
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('id')
            quantity = int(data.get('quantity', 1))

            product = Produce.objects.get(pk=product_id)
            CartItem.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

@login_required(login_url='login')
def get_cart_items(request):
    cart_items = CartItem.objects.filter(user=request.user)
    data = []

    for item in cart_items:
        data.append({
            'id': item.product.id,
            'name': item.product.name.name,
            'price': item.product.price,
            'quantity': item.quantity,
        })

    return JsonResponse(data, safe=False)



@csrf_exempt
@login_required
def update_cart_item(request):
    json_error = []
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produce_id = data.get('id')
            quantity = int(data.get('quantity'))
            if quantity < 0:
                json_error.append('Username is required')
            
            if json_error:
             return JsonResponse({'error': json_error}, status=400)
            

            cart_item = CartItem.objects.get(user=request.user, product_id=produce_id)
            cart_item.quantity = quantity
            cart_item.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

from django.views.decorators.http import require_POST

@csrf_exempt
@login_required
@require_POST
def remove_cart_item(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('id')

        CartItem.objects.filter(user=request.user, product_id=product_id).delete()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
