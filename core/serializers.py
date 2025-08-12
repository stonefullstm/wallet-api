from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'sticker', 'company_name', 'company_full_name']
        read_only_fields = ['id']

    def validate_sticker(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Sticker must be alphanumeric.")
        return value.upper()
