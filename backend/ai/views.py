from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class GenerateMail(APIView):
    def get(self, request, *args, **kwargs):
        return Response("This is test")