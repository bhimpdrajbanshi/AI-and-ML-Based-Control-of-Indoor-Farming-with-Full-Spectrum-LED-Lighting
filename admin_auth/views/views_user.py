from django.shortcuts import render
from ..global_func import checkUserExist
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from ..models import Produce
from django.contrib import messages
from django.views.decorators.http import require_POST

from django.contrib.auth import get_user_model


User = get_user_model()

def user_list(request):
    users = User.objects.all() 
    context = {
        'users': users
    }
    return render(request, 'admin/user_list.html', context)

def delete_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('user_list')

    return render(request, 'delete_user.html', {'user': user})

def edit_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return redirect('admin-dashboard')

    return render(request, 'admin/edit_user.html', {'user': user})
