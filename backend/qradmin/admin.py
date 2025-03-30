from django.contrib import admin
from qradmin.models import QRCode, QRBatch, CompanyWallet

# Register your models here.

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ("qr_number","batch","point","qr_code","is_used","used_by","is_disabled")

@admin.register(QRBatch)
class QRBatchAdmin(admin.ModelAdmin):
    list_display = ("batch_number","total_amount", "total_point","point_per_amount", "point_per_qr")

@admin.register(CompanyWallet)
class CompanyWalletAdmin(admin.ModelAdmin):
    list_display = ("company", "amount_limit","total_amount","total_point","total_user_amount","total_user_point","total_withdraw_amount",'total_withdraw_point')