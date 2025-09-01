from rest_framework import serializers
from .models import Stock, WalletConfig


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'ticker', 'company_name', 'company_full_name']
        read_only_fields = ['id']

    def validate_sticker(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Ticker must be alphanumeric.")
        return value.upper()


class HistorySerializer(serializers.Serializer):
    date = serializers.DateField()
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    close = serializers.FloatField()
    volume = serializers.FloatField()


class MaxMinSerializer(serializers.Serializer):
    ticker = serializers.CharField()
    previous_close = serializers.FloatField()
    actual_close = serializers.FloatField()
    alta_baixa = serializers.FloatField()


class WalletConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletConfig
        fields = ['id', 'stock_date']
        read_only_fields = ['id']
