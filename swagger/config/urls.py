from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from configapp.api_views import (
    AccountViewSet,
    TransactionViewSet,
    CategoryViewSet,
    RecurringPaymentViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Bank Management API",
        default_version='v1',
        description="Bank API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'recurring-payments', RecurringPaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
]
