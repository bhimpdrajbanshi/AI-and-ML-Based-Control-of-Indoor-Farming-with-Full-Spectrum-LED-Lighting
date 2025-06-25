
from django.contrib.auth import authenticate
from django.http import JsonResponse
def checkUserExist(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        if not user_name or not password:
            return JsonResponse({'success': False, 'message': 'Username and password are required.'})

        user = authenticate(username=user_name, password=password)
        if user is not None:
            return JsonResponse({'success': True, 'message': 'User exists and credentials are correct.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password.'})
    
    return JsonResponse({'success': False, 'message': 'Only POST method is allowed.'})