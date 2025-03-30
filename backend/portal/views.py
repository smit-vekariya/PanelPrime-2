from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


# Create your views here.

class DashBoardView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "portal/dashboard.html"
    
    
    def get(self, request, *args, **kwargs):
        context = {"message": "Welcome to the Dashboard"} 
        return Response(context)