from django.shortcuts import render
from rest_framework.views import APIView, View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from manager.manager import HttpsAppResponse, Util
from app.serializers import *
from django.contrib import messages
from django.shortcuts  import redirect
from django.urls import reverse
from app.serializers import CommentQuestionsSerializers, CommentAnswerSerializers, ContactUsSerializers
from app.models import CommentQuestions, CommentAnswer
from rest_framework import viewsets
from rest_framework import filters
import json
from django.utils import timezone
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from rest_framework.decorators import action
from manager.serializers import PeriodicTaskSerializer, TaskResultSerializer
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, ClockedSchedule
from app.forms import PeriodicTaskForm
from manager.decorators import query_debugger
from django_celery_results.models import TaskResult
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class MessageView(APIView):
    authentication_classes =[]
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/message.html"

    def get(self, request, *args, **kwargs):
        return Response(status=200, template_name=self.template_name, data={"messages":request.GET.get("messages")})

class Welcome(APIView):
    authentication_classes =[]
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/welcome.html"

    def get(self, request, *args, **kwargs):
        return Response(status=200, template_name=self.template_name)


class AskAnything(LoginRequiredMixin, viewsets.ModelViewSet):
    # we use LoginRequiredMixin because we need django default authentication not  
    login_url = '/account/app_login/'
    queryset = CommentQuestions.objects.all()
    serializer_class = CommentQuestionsSerializers
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/ask_anything.html"
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)
        return Response(status=200, template_name=self.template_name,data={"question_answer":json.loads(json.dumps(serializer.data))})

    def create(self, request, *args, **kwargs):
        if "answer_textarea" in request.POST:
            answer_textarea = request.POST.get("answer_textarea")
            question_id = request.POST.get("question_id")
            serializer = CommentAnswerSerializers(data={"answer":answer_textarea, "created_on":timezone.now(),'questions':question_id, 'action_by':request.user.id})
        else:
            question_textarea = request.POST.get("question_textarea")
            serializer = self.serializer_class(data={"question":question_textarea,"created_on":timezone.now(), 'action_by':request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return redirect(reverse('app:ask-anything-page'))

    def destroy_answer(self, request, *args, **kwargs):
        instance = CommentAnswer.objects.get(pk=kwargs['pk'])
        instance.delete()
        return HttpsAppResponse.send([], 1, "Delete Answer successfully.")

    def update_answer(self, request, *args, **kwargs):
        instance = CommentAnswer.objects.get(pk=kwargs['pk'])
        serializer = CommentAnswerSerializers(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return HttpsAppResponse.send([], 1, "Update answer successfully.")


class AboutUs(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/about_us.html"

    def get(self, request, *args, **kwargs):
        return Response(status=200, template_name=self.template_name)   


class ContactUs(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ContactUsSerializers
    template_name = "app/contact_us.html"

    def get(self, request, *args, **kwargs):
        return Response(status=200, template_name=self.template_name) 

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect(reverse('app:message-page') + '?messages=We recived your query. We will contact you soon.')
            else:
                return redirect(reverse('app:message-page') + '?messages=Something went wrong! Try later.')
        except Exception as e:
            return HttpsAppResponse.exception(str(e))
            

class TaskSchedulerView(LoginRequiredMixin, viewsets.ModelViewSet):
    login_url = '/account/app_login/'
    queryset = PeriodicTask.objects.all().select_related('interval','crontab','clocked')
    serializer_class = PeriodicTaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields =["name","task"]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/task_scheduler.html"

    def list(self, request, *args, **kargs):
        queryset = self.get_queryset()
        serializers = self.get_serializer(queryset, many=True)
        periodic_id = self.request.query_params.get("id")
        if periodic_id:
            periodic_form = PeriodicTaskForm(instance=queryset.get(id=periodic_id))
            form_title= "Update Periodic Task"
        else:
            periodic_form = PeriodicTaskForm()
            form_title= "Create Periodic Task"
        return Response(status=200, template_name=self.template_name, data={"task_scheduler_list":serializers.data, "periodic_form":periodic_form, "form_title":form_title, "periodic_id":periodic_id})        

    def task_operation(self, request, *args, **kargs):
        try:
            object_ = self.get_object()
            query_param = self.request.query_params.get("operation")
            if query_param == "delete":
                object_.delete()
                return HttpsAppResponse.send([], 1, f"Task {query_param} successfully.")
            elif query_param == "enable":
                object_.enabled = True
            elif query_param =="disable":
                object_.enabled = False
            object_.save()
            return HttpsAppResponse.send([], 1, f"Task {query_param} successfully.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))

    def update_create(self, request, *args, **kargs):
        queryset = self.get_queryset()
        periodic_id = request.POST.get("periodic_id")
        if periodic_id and periodic_id != "None":
            periodic_form = PeriodicTaskForm(request.POST, instance=queryset.get(id=periodic_id))
        else:
            periodic_form = PeriodicTaskForm(request.POST)
        if periodic_form.is_valid():
            periodic_form.save()
            return redirect(reverse('app:task-scheduler-page'))
        else:
            serializers = self.get_serializer(queryset, many=True)
            return Response(status=200, template_name=self.template_name, data={"task_scheduler_list":serializers.data, "periodic_form":periodic_form}) 
            
    def task_result(self,request, *args, **kwargs):
        periodic_name = self.request.query_params.get('periodic_name')
        results = TaskResult.objects.filter(periodic_task_name=periodic_name)
        if results:
            serializer = TaskResultSerializer(results, many=True)
            return Response(status=200, template_name="app/task_results_m.html", data={"results":serializer.data})
        return HttpResponse("Periodic task result not found.")   

