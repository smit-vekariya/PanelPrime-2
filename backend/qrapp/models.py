from django.db import models
from account.models import BondUser
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import transaction
from django.db.models import F
from decimal import Decimal
# Create your models here.


class BondUserWallet(models.Model):
    user = models.ForeignKey(BondUser, on_delete=models.CASCADE)
    total_earning_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_earning_point = models.IntegerField(default=0, null=True, blank=True)
    point = models.IntegerField(default=0, null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    withdraw_point = models.IntegerField(default=0, null=True, blank=True)
    withdraw_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    wallet_disabled = models.BooleanField(default=False)
    credit_disabled = models.BooleanField(default=False)
    debit_disabled = models.BooleanField(default=False)
    reason_disabled = models.TextField(null=True, blank=True)


    def __str__(self):
        return str(self.user)


transaction_types = (("credit","Credit"), ("debit","Debit"))
class Transaction(models.Model):
    wallet =models.ForeignKey(BondUserWallet, on_delete=models.PROTECT)
    description = models.TextField()
    tran_type = models.CharField(max_length=100, choices=transaction_types)
    point = models.IntegerField(null=True, blank=True,default=0)
    total_point = models.IntegerField(null=True, blank=True,default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tran_on = models.DateTimeField(auto_now=True)
    tran_by = models.ForeignKey(BondUser, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            print('Update is not possible after transaction')
            return

        with transaction.atomic():
            if self.tran_type == "credit":
                point_per_amount = Decimal(settings.POINT_PER_AMOUNT)
                amount = Decimal(self.point) / point_per_amount
                wallet = self.wallet
                wallet.balance += amount
                wallet.point += self.point
                wallet.total_earning_amount += amount
                wallet.total_earning_point += self.point
                wallet.save()
                self.amount = amount
            elif self.tran_type == "debit":
                point_per_amount = Decimal(settings.POINT_PER_AMOUNT)
                point = Decimal(self.amount) * point_per_amount
                wallet = self.wallet
                wallet.balance -= self.amount
                wallet.point -= point
                wallet.withdraw_balance += self.amount
                wallet.withdraw_point += point
                wallet.save()
                self.point = point

            self.total_point = wallet.point
            self.total_amount = wallet.balance
            super().save(*args, **kwargs)


wallet_action_types = (
    ("credit_point", "Credit Point"),
    ("debit_point", "Debit Point"),
    ("w_money", "Withdraw Money"),
    ("error", "Error")
)

class WalletHistory(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id =  models.IntegerField(null=True, blank=True)
    action = models.TextField()
    action_type = models.CharField(max_length=100, choices=wallet_action_types, null=True, blank=True)
    ip_addr = models.CharField(default="", max_length=45)
    action_on = models.DateTimeField(auto_now=True)
    action_by = models.ForeignKey(BondUser, on_delete=models.PROTECT)
