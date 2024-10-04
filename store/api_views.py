from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Cart, Review, Order
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, ReviewSerializer, OrderSerializer, LoginSerializer, UserSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken


def api_root(request):
    api_endpoints = [
        "Categories: /api/categories/",
        "Subcategories: /api/subcategories/",
        "Products: /api/products/",
        "Orders: /api/orders/",
        "Cart: /api/cart/",
        "Reviews: /api/reviews/",
        "Register: /api/register/",
        "Login: /api/login/",
        "Logout: /api/logout/",
    ]
    
    
    response_text = "\n".join(api_endpoints)
    return HttpResponse(response_text, content_type="text/plain")

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        parent_categories = Category.objects.filter(parent_category__isnull=True)
        serializer = CategorySerializer(parent_categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def subcategory_list(request, category_id):
    try:
        parent_category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        subcategories = Category.objects.filter(parent_category=parent_category)
        serializer = CategorySerializer(subcategories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent_category=parent_category)  # Link the new subcategory to the parent
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def subcategory_detail(request, pk):
    try:
        subcategory = Category.objects.get(pk=pk, parent_category__isnull=False)  # Ensuring it's a subcategory
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(subcategory)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductList(APIView):
   
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CartList(APIView):
    def get(self, request):
        carts = Cart.objects.all()
        user = request.GET.get('user')
        if user:
            carts = carts.filter(user_id=user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.save()
            products = request.data.get('products', [])
            if products:
                cart.products.set(products)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetail(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            products = request.data.get('products', [])
            if products:
                cart.products.set(products)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_object(pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'user', 'rating']


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer




class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'status', 'created_at']


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




class SignupAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": True,
                "message": "User created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    "status": True,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({
                "status": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)