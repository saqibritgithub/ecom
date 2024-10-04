from django.urls import path
from . import api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', api_views.api_root, name='api-root'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Category URLs (Function-based views)
    path('categories/', api_views.category_list, name='category-list'),
    path('categories/<int:pk>/', api_views.category_detail, name='category-detail'),

    # SubCategory URLs (Function-based views)
    path('categories/<int:category_id>/subcategories/', api_views.subcategory_list, name='subcategory-list'),
    path('subcategories/<int:pk>/', api_views.subcategory_detail, name='subcategory-detail'),

    # Signup and Login URLs (Class-based views)
    path('signup/', api_views.SignupAPI.as_view(), name='signup'),
    path('login/', api_views.LoginAPI.as_view(), name='login'),

    # Product URLs (Class-based views)
    path('products/', api_views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', api_views.ProductDetail.as_view(), name='product-detail'),

    # Cart URLs (Class-based views)
    path('carts/', api_views.CartList.as_view(), name='cart-list'),
    path('carts/<int:pk>/', api_views.CartDetail.as_view(), name='cart-detail'),

    # Review URLs (Generic views)
    path('reviews/', api_views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', api_views.ReviewDetail.as_view(), name='review-detail'),

    # Order URLs (Generic views)
    path('orders/', api_views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', api_views.OrderDetail.as_view(), name='order-detail'),
]
