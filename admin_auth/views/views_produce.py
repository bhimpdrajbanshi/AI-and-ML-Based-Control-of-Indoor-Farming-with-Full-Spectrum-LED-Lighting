from django.shortcuts import render
from ..global_func import checkUserExist
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from ..models import Produce
from django.contrib import messages
from django.views.decorators.http import require_POST
from ..models import Vegetable

from django.contrib.auth import get_user_model


User = get_user_model()

def farmer_produce(request):
    produce_list  = Produce.objects.filter(created_by=request.user).all()
    vegetables = Vegetable.objects.all()
    context = {
        'produce_list': produce_list,
        'vegetables': vegetables
        }
    return render(request, 'farmer/produce.html', context) 


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

@login_required
def save_produce(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'errors': ['Invalid JSON']}, status=400)

        name = data.get('produceName')
        quantity = data.get('quantityAvailable')
        price = data.get('pricePerKg')
        certification = data.get('certification', 'safe_food')
        remarks = data.get('remarks', '')

        errors = []

        if not name:
            errors.append('Produce name is required.')
        if not quantity or not str(quantity).replace('.', '', 1).isdigit():
            errors.append('Valid quantity is required.')
        if not price or not str(price).replace('.', '', 1).isdigit():
            errors.append('Valid price is required.')

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        try:
            Produce.objects.create(
                name_id=name,  # ForeignKey to Vegetable
                quantity=float(quantity),
                price=float(price),
                certification=certification,
                remarks=remarks,
                created_by=request.user
            )
        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': [str(e)]}, status=500)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'invalid method'}, status=405)




def delete_produce(request, id):
    produce = get_object_or_404(Produce, id=id)
    produce.delete()
    return redirect('farmer-produce')


def edit_produce(request, id):
    produce = get_object_or_404(Produce, id=id)

    if request.method == 'POST':
        produce.name = request.POST.get('produceName')
        produce.quantity = request.POST.get('quantityAvailable')
        produce.price = request.POST.get('pricePerKg')
        produce.certification = request.POST.get('certification')
        produce.remarks = request.POST.get('remarks')
        produce.save()
        return redirect('farmer-dashboard')

    return render(request, 'farmer/edit.html', {'produce': produce})