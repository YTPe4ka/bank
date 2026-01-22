"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from configapp.api_views import (
    UserRegisterViewSet, UserViewSet, CategoryViewSet,
    AccountViewSet, TransactionViewSet, RecurringPaymentViewSet
)
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView

# API Router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'register', UserRegisterViewSet, basename='register')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'recurring-payments', RecurringPaymentViewSet, basename='recurring-payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # API Documentation - Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/', include(router.urls)),
]
