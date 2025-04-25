from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('product/edit/', views.product_edit, name='product_edit_new'),
    path('product/delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('orders/<int:year>/<int:month>/', views.order_summary, name='order_summary'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.products_by_category, name='products_by_category'),
]