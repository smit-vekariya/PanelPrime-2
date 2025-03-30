from django.urls import path, include
from .views import *
from .portfolio_views import *
from rest_framework.routers import DefaultRouter

app_name = "app"

urlpatterns = [
    path('', Welcome.as_view(), name="welcome-page"),
    path('ask_anything/', AskAnything.as_view({'get': 'list', 'post':'create'}), name="ask-anything-page"),
    path('ask_anything/<int:pk>/', AskAnything.as_view({'delete': 'destroy','patch':'partial_update'}), name="ask-anything-page-detail"),
    path('delete_update_answer/<int:pk>/', AskAnything.as_view({'delete': 'destroy_answer','put':'update_answer'}), name="delete-update-detail"),
    path('about_us/', AboutUs.as_view(), name="about-us-page"),
    path('contact_us/', ContactUs.as_view(), name="contact-us-page"),  
    path('message/', MessageView.as_view(), name="message-page"),  
    path('task_scheduler/', TaskSchedulerView.as_view({'get':'list','post':'update_create'}), name="task-scheduler-page"),
    path('task_scheduler_operation/<int:pk>/', TaskSchedulerView.as_view({'get':'task_operation'}), name="task-scheduler-operation"),
    path('task_scheduler_result/', TaskSchedulerView.as_view({'get':'task_result'}), name="task-result"),
    path("portfolio/", PortFolioView.as_view(), name="portfolio-index")
]