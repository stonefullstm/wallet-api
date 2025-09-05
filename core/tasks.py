from datetime import date, datetime
from .models import HistoryStock, Stock, WalletConfig
from .serializers import (
    StockSerializer,
)
import yfinance as yf


def update_history_stock():
    print(f"Executando atualização às {datetime.now()}")
    tickers = StockSerializer(Stock.objects.all(), many=True).data
    ticker_list = [ticker["ticker"] + ".SA" for ticker in tickers]
    config = WalletConfig.objects.first()
    multiple_tickers = yf.download(
        ticker_list,
        period="2d",
        interval="1d",
        multi_level_index=False,
        ignore_tz=True,
        auto_adjust=False,
    )[["Close", "Volume"]].T.dropna()
    for index, row in multiple_tickers.iterrows():
        if index[0] == "Close":
            HistoryStock.objects.update_or_create(
                ticker=index[1].replace(".SA", ""),
                defaults={
                    "previous_close": float(row.iloc[0]),
                    "actual_close": float(row.iloc[1]),
                    "alta_baixa": float(
                        ((row.iloc[1] - row.iloc[0]) / row.iloc[1]) * 100
                    ),
                    "volume": float(
                      multiple_tickers.loc[("Volume", index[1])].iloc[1]),
                    "date": multiple_tickers.columns[1].strftime("%Y-%m-%d"),
                },
            )
    config.history_date = date.today()
    config.save()
