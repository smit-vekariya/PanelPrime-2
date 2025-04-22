
from django.urls import path, include
from .views import *

app_name = "ai"

urlpatterns = [
    path('generate_mail/', GenerateMail.as_view(), name='generate_mail'),
]