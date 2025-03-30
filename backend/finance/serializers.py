from finance.models import FinUser, Transactions, ITCompany
from rest_framework import serializers

class FinUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = FinUser
        fields = '__all__'


class TransactionsSerializers(serializers.ModelSerializer):
    class Meta:
        model =Transactions
        fields= '__all__'
    

class UserTransSerializers(serializers.ModelSerializer):
    trans = TransactionsSerializers(source='transactions_set', many=True, read_only=True)
    class Meta:
        model = FinUser
        fields = ("id", "name", "income", "expence", "trans")


class ITCompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = ITCompany
        fields = '__all__'