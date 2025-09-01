from django.db import models


# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=6, unique=True)
    company_name = models.CharField(max_length=100)
    company_full_name = models.CharField(max_length=100)
    excluded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ticker} - {self.company_name}"


class WalletConfig(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    stock_date = models.DateField()

    def __str__(self):
        return f"WalletConfig for {self.stock_date}"
