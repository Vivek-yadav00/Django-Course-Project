from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker=models.CharField(max_length=10)
    company_name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=5)

    def __str__(self):
        return self.ticker  