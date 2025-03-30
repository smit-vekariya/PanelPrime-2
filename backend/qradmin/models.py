from django.db import models
from account.models import BondUser, Company

# Create your models here.
class CompanyWallet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    amount_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_point =  models.IntegerField(null=True, blank=True, default=0)
    total_user_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_user_point = models.IntegerField(null=True, blank=True, default=0)
    total_withdraw_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdraw_point = models.IntegerField(null=True, blank=True, default=0)

class QRBatch(models.Model):
    batch_number = models.CharField(unique=True, max_length=20)
    total_qr_code = models.IntegerField(null=True, blank=True, default=0)
    total_used_qr_code = models.IntegerField(null=True, blank=True, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    point_per_amount = models.IntegerField(null=True, blank=True, default=0)
    total_point = models.IntegerField(null=True, blank=True, default=0)
    point_per_qr = models.IntegerField(null=True, blank=True, default=0)
    amount_per_qr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_by = models.ForeignKey(BondUser, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_printed = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    expire_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.batch_number)


class QRCode(models.Model):
    qr_number = models.CharField(unique=True, max_length=20)
    qr_code = models.CharField(unique=True, max_length=50)
    batch = models.ForeignKey(QRBatch, on_delete=models.PROTECT)
    point = models.IntegerField(null=True, blank=True, default=0)
    used_on = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(BondUser, on_delete=models.CASCADE, null=True, blank=True)
    is_printed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_used= models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.qr_number)

