from django.contrib import admin
from django.urls import path
from core.views import HistoryViewSet, StockViewSet, WalletConfigViewSet
from user.views import UserCreateAPIView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = routers.DefaultRouter()
# router.register(r'stocks', StockViewSet)
# router.register(
#     r'wallet-config', WalletConfigViewSet, basename='wallet-config'
#     )

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "history/get-last-day/",
        HistoryViewSet.as_view({"get": "get_last_day"}),
        name="get-last-day"),
    path(
        # "history/retrieve/<str:ticker>/<str:start_date>/<str:end_date>/<str:interval>",
        "history/retrieve/<str:ticker>/",
        HistoryViewSet.as_view({"get": "retrieve"}), name="history-retrieve"),

    path("stocks/", StockViewSet.as_view(), name="stock-list"),
    path("wallet-config/list/", WalletConfigViewSet.as_view({"get": "list"})),
    path(
        "wallet-config/get-date/<int:pk>/",
        WalletConfigViewSet.as_view({"get": "get_date"}),
    ),
    path("user/", UserCreateAPIView.as_view(), name="user-create"),
    path(
         "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
     ),
    path(
         "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
     ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
