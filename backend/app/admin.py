from django.contrib import admin
from app.models import ContactUs, CommentQuestions, CommentAnswer
# Register your models here.

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("full_name","mobile","email","subject", "resolved")

@admin.register(CommentQuestions)
class CommentQuestionsAdmin(admin.ModelAdmin):
    list_display = ("question",)

@admin.register(CommentAnswer)
class CommentAnswerAdmin(admin.ModelAdmin):
    list_display= ("questions","answer")