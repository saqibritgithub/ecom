from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)
    parent_category = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='subcategories', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='carts')

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'

class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return f'Order {self.id} by {self.user.username if self.user else "Guest"}'
    
    from django.db import models

from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    date_posted = models.DateField()
    #catagory = models.CharField(max_length=255, null=True, blank=True)  # Optional field for job category
    lead_date = models.DateField(null=True, blank=True)
    platform = models.CharField(max_length=255, null=True, blank=True)
    lead_url = models.URLField(null=True, blank=True)
    company_url = models.URLField(null=True, blank=True)
    posted_date = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    job_fetch_timestamp = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)
    company_url_validated = models.BooleanField(default=False)
    already_exist_validated = models.BooleanField(default=False)
    invalid_title_validated = models.BooleanField(default=False)
    email_validated = models.EmailField(max_length=255, null=True, blank=True)
    validated_date = models.DateField(null=True, blank=True)
    posted_date_formatted = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
