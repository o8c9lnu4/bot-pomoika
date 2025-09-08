"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from blog.views import PostViewSet, home_view, post_detail_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'posts', PostViewSet)

def debug_view(request):
    return HttpResponse(f"Path: {request.path}, Method: {request.method}, Headers: {request.headers}")

# Сначала определяем все Django URL
urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # Главная страница
    path('', home_view, name='home'),
    path('post/<int:post_id>/', post_detail_view, name='post_detail'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/', include('blog.urls')),
    
    # Отладочный URL
    path('debug/', debug_view),
]

# Статические файлы
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

# Vue.js routes (исключаем admin, api и static)
urlpatterns += [
    re_path(r'^(?!admin/|api/|static/|debug/).*$', TemplateView.as_view(template_name='index.html')),
]
