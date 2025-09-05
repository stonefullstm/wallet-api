from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from services.stocks import get_b3_stock_codes
from .models import HistoryStock, Stock, WalletConfig
from .serializers import (
    MaxMinSerializer,
    StockSerializer,
    WalletConfigSerializer,
    HistorySerializer,
)
from datetime import date
import yfinance as yf


# Create your views here.
class HistoryViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"])
    def retrieve(
        self,
        request,
        ticker,
        # start_date,
        # end_date,
        # interval="1d",
        pk=None,
    ):
        if ticker[0] != "^":
            ticker = ticker + ".SA"
        # start_date = datetime.strptime(start_date, "%Y-%m-%d")
        # end_date = datetime.strptime(end_date, "%Y-%m-%d")
        # ticker = request.GET.get("ticker") + ".SA"
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        interval = request.GET.get("interval", "1d")
        stock = yf.Ticker(ticker)
        history = stock.history(
            start=start_date, end=end_date, interval=interval)
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
            HistorySerializer(history_array, many=True).data)

    @action(detail=False, methods=["get"])
    def get_last_day(self, request):
        # tickers = StockSerializer(Stock.objects.all(), many=True).data
        # ticker_list = [ticker["ticker"] + ".SA" for ticker in tickers]
        # config = WalletConfig.objects.first()
        # if config:
        #     if config.history_date != date.today():
        #         multiple_tickers = yf.download(
        #             ticker_list,
        #             period="2d",
        #             interval="1d",
        #             multi_level_index=False,
        #             ignore_tz=True,
        #             auto_adjust=False,
        #         )[["Close", "Volume"]].T.dropna()
        #         for index, row in multiple_tickers.iterrows():
        #             if index[0] == "Close":
        #                 HistoryStock.objects.update_or_create(
        #                     ticker=index[1].replace(".SA", ""),
        #                     defaults={
        #                         "previous_close": float(row.iloc[0]),
        #                         "actual_close": float(row.iloc[1]),
        #                         "alta_baixa": float(
        #                             (
        #                                 (row.iloc[1] - row.iloc[0])
        #                                 / row.iloc[1]
        #                             ) * 100
        #                         ),
        #                         "volume": float(
        #                             multiple_tickers.loc[
        #                                 ("Volume", index[1])].iloc[1]
        #                         ),
        #                         "date": multiple_tickers.columns[1].strftime(
        #                             "%Y-%m-%d"
        #                         ),
        #                     },
        #                 )
        #         config.history_date = date.today()
        #         config.save()
        return Response(
                MaxMinSerializer(
                    HistoryStock.objects.all(), many=True
                ).data
            )
        # return Response(
        #     {"error": "No wallet configuration found."}, status=404)


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
