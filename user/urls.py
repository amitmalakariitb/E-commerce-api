from django.urls import path
from .views import register_user, user_login, user_logout , add_new_address , edit_saved_addresses , view_saved_addresses , prime_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add_new_address/', add_new_address, name='add_new_address'),
    path('edit_saved_addresses/<str:pk>', edit_saved_addresses, name='edit_saved_addresses'),
    path('view_saved_addresses/<str:pk>', view_saved_addresses, name='view_saved_addresses'),
    path('primeuser/', prime_user, name='primeuser')
]