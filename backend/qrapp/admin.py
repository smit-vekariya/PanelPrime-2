from django.contrib import admin
from qrapp.models import BondUserWallet, Transaction, WalletHistory

# Register your models here.
@admin.register(BondUserWallet)
class MainMenuBondUserWallet(admin.ModelAdmin):
    list_display = ("user","point","balance","withdraw_point","withdraw_balance")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'description', 'tran_type', 'point','total_point', 'amount','total_amount', 'tran_on', 'tran_by')

@admin.register(WalletHistory)
class WalletHistoryAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'action', 'action_type', 'ip_addr', 'action_on', 'action_by')
