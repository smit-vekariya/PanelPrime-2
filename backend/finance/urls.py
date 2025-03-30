from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance.views import *

app_name = "finance"

router = DefaultRouter()
router.register(r'companies', CompaniesView, basename="companies")
router.register(r'', DashBoardView, basename="finance-dashboard")

urlpatterns = [
]
urlpatterns += router.urls