from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from google import genai
from django.conf import settings
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class AskMeAnything(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            query_params = self.request.query_params
            query = query_params.get("query")
            qtype = query_params.get("qtype")
            if query:
                query = self.promt_filter(query, qtype)
                return self.ask_gemini(query)
            else:
                return Response("query not found!")
        except Exception as e:
            return Response(str(e))

    def promt_filter(self, query, qtype):
        if qtype == "mail":
            query = "Generate a professional email message part only not subjects and other. The 'message' should include proper formatting with line breaks (\\n). Here's the context:" + query
        return query

    def ask_gemini(self, query):
        try:
            response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[query]
                    )
            return Response(response.text)
        except Exception as e:
            return Response(str(e))


