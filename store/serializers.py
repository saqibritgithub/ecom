from rest_framework import serializers
from .models import Category, Product, Cart, Review, Order, Job
from django.contrib.auth.models import User

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    image = serializers.ImageField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Foreign key to Category
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    def create(self, validated_data):
        cart = Cart.objects.create(user=validated_data['user'])
        cart.products.set(validated_data['products'])
        return cart

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.products.set(validated_data.get('products', instance.products.all()))
        instance.save()
        return instance
class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    rating = serializers.IntegerField()
    comment = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.user = validated_data.get('user', instance.user)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(max_length=100, default='Pending')

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        """Check if the email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class JobSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    company = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    job_type = serializers.CharField(max_length=255)
    date_posted = serializers.DateField()
    # lead_date = serializers.DateField(allow_null=True, required=False)
    # platform = serializers.CharField(max_length=255, allow_null=True, required=False)
    # lead_url = serializers.URLField(allow_null=True, required=False)
    # company_url = serializers.URLField(allow_null=True, required=False)
    # posted_date = serializers.DateField(allow_null=True, required=False)
    # region = serializers.CharField(max_length=255, allow_null=True, required=False)
    # industry = serializers.CharField(max_length=255, allow_null=True, required=False)
    # job_fetch_timestamp = serializers.DateTimeField(read_only=True)
    # validated = serializers.BooleanField(default=False)
    # company_url_validated = serializers.BooleanField(default=False)
    # already_exist_validated = serializers.BooleanField(default=False)
    # invalid_title_validated = serializers.BooleanField(default=False)
    # email_validated = serializers.EmailField(allow_null=True, required=False)
    # validated_date = serializers.DateField(allow_null=True, required=False)
    # posted_date_formatted = serializers.CharField(max_length=255, allow_null=True, required=False)

    def create(self, validated_data):
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
 
class GroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    company = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    job_type = serializers.CharField(max_length=255)

class IdSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    company = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    job_type = serializers.CharField(max_length=255)
