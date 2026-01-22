"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from configapp.api_views import (
    UserRegisterViewSet, UserViewSet, CategoryViewSet,
    AccountViewSet, TransactionViewSet, RecurringPaymentViewSet
)
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

# API Router
router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='user')
router.register(r'api/register', UserRegisterViewSet, basename='register')
router.register(r'api/categories', CategoryViewSet, basename='category')
router.register(r'api/accounts', AccountViewSet, basename='account')
router.register(r'api/transactions', TransactionViewSet, basename='transaction')
router.register(r'api/recurring-payments', RecurringPaymentViewSet, basename='recurring-payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Swagger / API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # path('', include(router.urls)),
    path('', include('configapp.urls')),
]
