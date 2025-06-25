from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import UserProfile

@login_required
def profile_create(request):
    if request.method == 'POST':
        json_errors = []

        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        
        # File uploads
        bank_qr = request.FILES.get('bank_qr')
        citizenship = request.FILES.get('citizenship')
        photo = request.FILES.get('photo')

        if not all([full_name, email, phone, street, city, state, zip_code]):
            json_errors.append("All fields are required.")
        if len(phone) < 10:
           json_errors.append("Phone Number must be at least 10 characters.")
           
        profile = UserProfile.objects.filter(user_id=request.user.id).first()
        
        if profile:
            if UserProfile.objects.filter(email=email).exclude(id=profile.id).exists():
                json_errors.append("Email already exists.")
            
            if UserProfile.objects.filter(phone=phone).exclude(id=profile.id).exists():
                json_errors.append("Phone Number already exists.")
            
        if not bank_qr:
           json_errors.append("Bank QR is required.")
           
        if not citizenship:
           json_errors.append("Citizenship is required.")
        
        if not photo:
           json_errors.append("Passport size photo is required.")
        
        if json_errors:
            return JsonResponse({'error': json_errors}, status=400)

        user = request.user

        profile, created = UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'street': street,
                'city': city,
                'state': state,
                'zip_code': zip_code
            }
        )
         # Save uploaded documents if present
        if bank_qr:
            profile.bank_qr = bank_qr
        if citizenship:
            profile.citizenship = citizenship
        if photo:
            profile.photo = photo

        profile.save()

        # After saving redirect or send JSON success if using AJAX
        return redirect('profile-create')

    return render(request, 'farmer/profile/profile_create.html')



@login_required
def profile_get_data(request):
    try:
        profile = request.user.profile  # Assuming OneToOne relation named 'profile'
        data = {
            'fullName': profile.full_name,
            'email': profile.email,
            'phone': profile.phone,
            'street': profile.street,
            'city': profile.city,
            'state': profile.state,
            'zip': profile.zip_code,
            'bankQrUrl': profile.bank_qr.url if profile.bank_qr else '',
            'citizenshipUrl': profile.citizenship.url if profile.citizenship else '',
            'photoUrl': profile.photo.url if profile.photo else '',
        }
        return JsonResponse({'status': 'success', 'data': data})
    except UserProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f"Dear {request.user.username}, kindly complete the KYC form to proceed with the next steps in the process. Thank you for your cooperation."})
