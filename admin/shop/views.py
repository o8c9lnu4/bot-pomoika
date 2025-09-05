from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch
import json

from .models import Product, Category, Application


def categories_list(request):
    """Получить список категорий"""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    
    categories = list(Category.objects.values_list('name', flat=True))
    return JsonResponse(categories, safe=False)


def serialize_product(product):
    """Сериализация товара для API"""
    return {
        'id': product.id,
        'title': product.title,
        'description': product.description or '',
        'price': float(product.price),
        'category': product.category.name if product.category else None,
        'photo_url': product.photo_url,
        'strength': product.strength,
        'is_active': product.is_active,
        'flavors': [
            {'name': flavor.name, 'in_stock': flavor.in_stock}
            for flavor in product.flavors.all()
        ]
    }


@require_http_methods(["GET", "POST"])
def items_list(request):
    """Получить список товаров или создать новый"""
    if request.method == 'GET':
        # Фильтрация
        category = request.GET.get('category')
        q = request.GET.get('q')
        active_only = request.GET.get('active_only', 'true').lower() == 'true'
        
        queryset = Product.objects.select_related('category').prefetch_related('flavors')
        
        if active_only:
            queryset = queryset.filter(is_active=True)
        
        if category:
            queryset = queryset.filter(category__name=category)
        
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(description__icontains=q)
        
        products = [serialize_product(p) for p in queryset]
        return JsonResponse(products, safe=False)
    
    elif request.method == 'POST':
        # Создание нового товара
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Валидация обязательных полей
        required_fields = ['title', 'price', 'category']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        
        # Получение или создание категории
        category_name = data['category']
        category, created = Category.objects.get_or_create(name=category_name)
        
        # Создание товара
        product = Product.objects.create(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            category=category,
            strength=data.get('strength', ''),
            is_active=data.get('is_active', True)
        )
        
        # Создание вкусов
        flavors_data = data.get('flavors', [])
        for flavor_data in flavors_data:
            Flavor.objects.create(
                product=product,
                name=flavor_data.get('name', ''),
                in_stock=flavor_data.get('in_stock', True)
            )
        
        return JsonResponse(serialize_product(product), status=201)


@require_http_methods(["GET", "PUT", "DELETE"])
def item_detail(request, pk):
    """Получить, обновить или удалить товар"""
    try:
        product = Product.objects.select_related('category').prefetch_related('flavors').get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(serialize_product(product))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Обновление полей товара
        if 'title' in data:
            product.title = data['title']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'strength' in data:
            product.strength = data['strength']
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        # Обновление категории
        if 'category' in data:
            category_name = data['category']
            category, created = Category.objects.get_or_create(name=category_name)
            product.category = category
        
        product.save()
        
        # Обновление вкусов
        if 'flavors' in data:
            # Удаляем старые вкусы
            product.flavors.all().delete()
            # Создаем новые
            for flavor_data in data['flavors']:
                Flavor.objects.create(
                    product=product,
                    name=flavor_data.get('name', ''),
                    in_stock=flavor_data.get('in_stock', True)
                )
        
        return JsonResponse(serialize_product(product))
    
    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'ok': True})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def applications_list(request):
    """Получить список заявок или создать новую"""
    if request.method == 'GET':
        applications = Application.objects.all().order_by('-created_at')
        data = []
        for app in applications:
            data.append({
                'id': app.id,
                'created_at': app.created_at.isoformat(),
                'customer_name': app.customer_name,
                'contact': app.contact,
                'status': app.status,
                'total_amount': float(app.total_amount),
                'items_count': app.items_count,
                'raw_payload': app.raw_payload
            })
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Создание заявки
        application = Application.objects.create(
            customer_name=data.get('customer_name', ''),
            contact=data.get('contact', ''),
            total_amount=data.get('total', 0),
            raw_payload=data
        )
        
        return JsonResponse({
            'id': application.id,
            'ok': True
        }, status=201)
