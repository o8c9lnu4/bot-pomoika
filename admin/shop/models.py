from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    strength = models.CharField(max_length=50, blank=True, verbose_name="Крепкость")
    photo = models.ImageField(upload_to="products/photos/", blank=True, null=True, verbose_name="Фото")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None


class Flavor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="flavors", verbose_name="Товар")
    name = models.CharField(max_length=100, verbose_name="Название вкуса")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Вкус"
        verbose_name_plural = "Вкусы"
        ordering = ['name']

    def __str__(self):
        return f"{self.product.title}: {self.name}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('processing', 'В обработке'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    customer_name = models.CharField(max_length=200, blank=True, verbose_name="Имя клиента")
    contact = models.CharField(max_length=200, blank=True, verbose_name="Контакт")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Сумма заказа")
    raw_payload = models.JSONField(verbose_name="Данные заказа")
    notes = models.TextField(blank=True, verbose_name="Заметки")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка #{self.id} от {self.created_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def items_count(self):
        if isinstance(self.raw_payload, dict):
            items = self.raw_payload.get('items', [])
            return len(items)
        return 0
