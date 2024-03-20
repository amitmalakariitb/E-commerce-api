from django.urls import path
from .views import add_to_cart,view_cart,edit_cart,direct_purchase,checkout,get_order_details
urlpatterns = [
    path('add_to_cart/' , add_to_cart,name = 'add_to_cart'),
    path('view_cart/<str:pk>' , view_cart,name = 'view_cart'),
    path('edit_cart/<str:pk>' , edit_cart,name = 'edit_cart'),
    path('direct_purchase/' , direct_purchase,name = 'create_order'),
    path('checkout/' , checkout,name = 'create_order_from_cart'),
    path('order/<int:order_id>/', get_order_details, name='get_order_details'),

]