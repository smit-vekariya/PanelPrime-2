
from django.urls import path, include
from .views import *

app_name = "ai"

urlpatterns = [
    path('ask_me_anything/', AskMeAnything.as_view(), name='ask_me_anything')
]