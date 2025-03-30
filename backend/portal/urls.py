from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portal.views import *

app_name = "portal"

# router = DefaultRouter()
# router.register(r'', DashBoardView, basename="dashboard")

urlpatterns = [
    path('', DashBoardView.as_view(), name="dashboard-view")
]
# urlpatterns += router.urls