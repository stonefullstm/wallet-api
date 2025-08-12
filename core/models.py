from django.db import models


# Create your models here.
class Stock(models.Model):
    sticker = models.CharField(max_length=6, unique=True)
    company_name = models.CharField(max_length=100)
    company_full_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sticker} - {self.company_name}"
