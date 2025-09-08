from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'blog'

urlpatterns = [
    path('', TemplateView.as_view(template_name='blog/index.html'), name='index'),
    path('auth/register/', views.register_view, name='register_api'),
    path('auth/login/', views.login_view, name='login_api'),
    path('auth/logout/', views.logout_view, name='logout_api'),
    path('auth/profile/', views.user_profile, name='profile_api'),
] 