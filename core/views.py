from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Stock, WalletConfig
from .serializers import StockSerializer, WalletConfigSerializer


# Create your views here.
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class WalletConfigViewSet(viewsets.GenericViewSet):
    queryset = WalletConfig.objects.all()
    serializer_class = WalletConfigSerializer

    @action(detail=False, methods=['get'])
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_date(self, request, pk):
        config = self.get_object()
        serializer = self.get_serializer(config)
        return Response({'stock_date': serializer.data.config.stock_date})
