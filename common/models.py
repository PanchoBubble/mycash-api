from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=25)

class Stock(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=12, decimal_places=4, null=True)
    class Meta:
        unique_together = ('currency', 'owner',)