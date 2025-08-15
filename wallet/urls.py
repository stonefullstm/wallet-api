from django.contrib import admin
from django.urls import path
from core.views import StockViewSet, WalletConfigViewSet
from user.views import UserCreateAPIView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
# router.register(r'stocks', StockViewSet)
# router.register(
#     r'wallet-config', WalletConfigViewSet, basename='wallet-config'
#     )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("stocks/", StockViewSet.as_view(), name="stock-list"),
    path("wallet-config/list/", WalletConfigViewSet.as_view({"get": "list"})),
    path(
        "wallet-config/get-date/<int:pk>/",
        WalletConfigViewSet.as_view({"get": "get_date"}),
    ),
    path("user/", UserCreateAPIView.as_view(), name="user-create"),
    path("api/token/", TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
]
