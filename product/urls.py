from django.urls import path
from . import views

urlpatterns = [
    path("products", views.api_products),
    path("products/<str:pk>", views.api_product),
    path("categories", views.api_categories),
    path("categories/<str:pk>", views.api_category),
    path("<int:product_id>/submit_review", views.post_review), 
    path("reviews/delete_review", views.delete_review),
    path('categories/<str:category_id>/sort/<str:sort_by>', views.sort_products),
    path('products/<int:pk>/update', views.update_product),
    path('seller/create_seller', views.create_seller),
    path('seller/<int:seller_id>/products', views.seller_products),
    path('seller/<int:seller_id>/add_product', views.add_product),
    ]