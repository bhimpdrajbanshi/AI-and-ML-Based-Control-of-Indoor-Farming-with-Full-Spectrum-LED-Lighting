
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    
    # admin
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('certification/', certification, name='certification'),
    
    # user
    path('users/list', user_list, name='user_list'),
    path('users/edit/<int:user_id>/', edit_user_view, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user_view, name='delete_user'),
    path('users/status/<int:user_id>/', toggle_user_status, name='toggle_user_status'),

    
    # farmer
    path('farmer/dashboard', farmer_dashboard, name='farmer-dashboard'),
    path('farmer/produce', farmer_produce, name='farmer-produce'),
     
    path('save-produce/', save_produce, name='save_produce'),
    path('edit-produce/<int:id>/', edit_produce, name='edit_produce'),
    path('delete-produce/<int:id>/', delete_produce, name='delete_produce'),
    path('produce/<int:pk>/change-status/', change_produce_status, name='change_produce_status'),
    # path('api/latest/', views.get_latest_data, name='get_latest_data')
    
    # farmer Prifile
    path('farmer/profile/create', profile_create, name='profile-create'),
    path('api/profile/get/', profile_get_data, name='api-get-profile'),
    
    # Consumer 
    path('consumer', consumer, name='consumer'),
    path('get-consumer-data/', get_consumer_data, name='get_consumer_data'),
    
    path('vegetables/', vegetable_list, name='vegetable_list'),
    path('vegetables/add/', vegetable_create, name='vegetable_create'),
    path('vegetables/<int:pk>/edit/', vegetable_edit, name='vegetable_edit'),
    path('vegetables/<int:pk>/delete/', vegetable_delete, name='vegetable_delete'),
    
    # cart
    path('cart', cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-items/', views.get_cart_items, name='get_cart_items'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/', views.remove_cart_item, name='remove_cart_item'),

]
