from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from common.models import Currency

class ExpenseType(models.Model):
    # Not unique "Type" model since properties will be aplly for each
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250)

class Expense(models.Model):
    STATE_CHOICES = (
        ('Pending', _('Pending')),
        ('Paid', _('Paid'))
    )
    cost = models.DecimalField(max_digits=12, decimal_places=4, null=True)
    date = models.DateField(null=True)
    description = models.CharField(max_length=250)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='Pending') 
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(ExpenseType, on_delete=models.DO_NOTHING)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
