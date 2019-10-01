from django.db import models
from user.models import User
from common.models import Currency

class IncomeType(models.Model):
    # Not unique "Type" model since properties will be aplly for each
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250)

class Income(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=4, null=True)
    date = models.DateField(null=True)
    description = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(IncomeType, on_delete=models.DO_NOTHING)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)

