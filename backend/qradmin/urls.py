
from django.urls import path
from .views import *
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = "qradmin"
urlpatterns = [
    path("company_dashboard/", CompanyDashboard.as_view({'get': 'list'}), name="company_dashboard"),
    path("user_list/", UserList.as_view(), name="user_list"),
    path("qr_batch_list/", QRBatchList.as_view(), name="qr_batch_list"),
    path("qr_code_list/", QRCodeList.as_view(), name="qr_code_list"),
    path("create_qr_batch/", CreateQRBatch.as_view(), name="create_qr_batch"),
    path('user_wallet/', UserWallet.as_view(), name="user_wallet"),
    path("print_batch/", PrintBatch.as_view(), name="print_batch"),
    path("users_wallet_report/", UsersWalletReport.as_view(), name="users_wallet_report"),
    path("disable_qr_code/", DisableQRCode.as_view(), name="disable_qr_code")
]