from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.items_list, name='items_list'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('categories/', views.categories_list, name='categories_list'),
    path('applications/', views.applications_list, name='applications_list'),
]
