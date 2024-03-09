from django.urls import path
from .views import add_to_cart,view_cart,edit_cart,direct_purchase,checkout
urlpatterns = [
    path('add_to_cart/' , add_to_cart,name = 'add_to_cart'),
    path('view_cart/' , view_cart,name = 'view_cart'),
    path('edit_cart/<str:pk>' , edit_cart,name = 'edit_cart'),
    path('Direct_Purchase/' , direct_purchase,name = 'create_order'),
    path('Checkout/' , checkout,name = 'create_order'),
]