from  app.models import ContactUs
from rest_framework import serializers
from app.models import CommentQuestions,CommentAnswer
 
class ContactUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class CommentAnswerSerializers(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    action_by_name = serializers.CharField(source='action_by.full_name',read_only=True)
    class Meta:
        model = CommentAnswer
        fields = ['id', 'answer','created_on','questions', 'action_by','action_by_name']
    

class CommentQuestionsSerializers(serializers.ModelSerializer):
    answers = CommentAnswerSerializers(many=True,read_only=True)
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    action_by_name = serializers.CharField(source='action_by.full_name',read_only=True)
    class Meta:
        model = CommentQuestions
        fields = ["id", "answers","question","created_on", 'action_by','action_by_name']

