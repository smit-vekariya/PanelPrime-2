
from django.urls import path, include
from .views import AskMeAnything
from .rag import DocQuestionAnswer, RagDocuments

app_name = "ai"

urlpatterns = [
    path('ask_me_anything/', AskMeAnything.as_view(), name='ask_me_anything'),
    path('rag_document/', RagDocuments.as_view(), name='rag_document'),
    path('doc_question_answer/', DocQuestionAnswer.as_view(), name='doc_question_answer')
]
