from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from services.stocks import get_b3_stock_codes
from .models import Stock, WalletConfig
from .serializers import (
    StockSerializer,
    WalletConfigSerializer,
    HistorySerializer
)
from datetime import date
import yfinance as yf


# Create your views here.
class HistoryViewSet(APIView):

    def get(
        self,
        request,
        ticker,
        start_date,
        end_date,
        interval="1d",
    ):
        ticker = ticker + ".SA"
        # start_date = datetime.strptime(start_date, "%Y-%m-%d")
        # end_date = datetime.strptime(end_date, "%Y-%m-%d")
        stock = yf.Ticker(ticker)
        history = stock.history(
            start=start_date, end=end_date, interval=interval
            )
        history_array = [
            {
                "date": index.strftime("%Y-%m-%d %H:%M:%S"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"]),
            }
            for index, row in history.iterrows()
        ]
        # return Response(HistorySerializer(history.to_dict()).data)
        return Response(
            {"history": HistorySerializer(history_array, many=True).data})


class StockViewSet(APIView):

    def get(self, request):
        config = WalletConfig.objects.first()
        if config:
            if config.stock_date != date.today():
                stock_data = get_b3_stock_codes()
                for stock in stock_data:
                    Stock.objects.update_or_create(
                        ticker=stock["ticker"],
                        defaults={
                            "company_name": stock["company_name"],
                            "company_full_name": stock["company_full_name"],
                        },
                    )
                config.stock_date = date.today()
                config.save()
            # print(date.today().strftime('%Y/%m/%d'))
            return Response(
                {
                    "stock_date": config.stock_date,
                    "stocks": StockSerializer(
                        Stock.objects.all(), many=True).data,
                }
            )
        return Response(
            {"error": "No wallet configuration found."}, status=404)


class WalletConfigViewSet(viewsets.GenericViewSet):
    queryset = WalletConfig.objects.all()
    serializer_class = WalletConfigSerializer

    @action(detail=False, methods=["get"])
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def get_date(self, request, pk):
        config = self.get_object()
        serializer = self.get_serializer(config)
        return Response({"stock_date": serializer.data["stock_date"]})
