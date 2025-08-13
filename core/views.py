from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from services.stocks import get_b3_stock_codes
from .models import Stock, WalletConfig
from .serializers import StockSerializer, WalletConfigSerializer
from datetime import date


# Create your views here.
class StockViewSet(APIView):

    def get(self, request):
        config = WalletConfig.objects.first()
        if config:
            if config.stock_date != date.today():
                stock_data = get_b3_stock_codes()
                for stock in stock_data:
                    Stock.objects.update_or_create(
                        sticker=stock['codigo'],
                        defaults={
                            'company_name': stock['nome'],
                            'company_full_name': stock['razao_social']
                        }
                    )
                config.stock_date = date.today()
                config.save()
            # print(date.today().strftime('%Y/%m/%d'))
            return Response({
                'stock_date': config.stock_date,
                'stocks': StockSerializer(Stock.objects.all(), many=True).data
                })
        return Response(
            {'error': 'No wallet configuration found.'}, status=404)


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
        return Response({'stock_date': serializer.data['stock_date']})
