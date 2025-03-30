from rest_framework import serializers
from account.models import BondUser ,City


# class UserSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields= '__all__'

#     def create(self, validate):
#         user =User(email=validate["email"],
#                    username=validate["username"],
#                    first_name=validate["first_name"],
#                    last_name=validate["last_name"])
#         user.set_password(validate["password"])
#         user.save()
#         return User

class BondUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = BondUser
        fields = '__all__'

        def create(self, validate):
            BondUser.objects.create(*validate)


class BondUserListSerializers(serializers.ModelSerializer):
    city__name = serializers.CharField(source='city.name', read_only=True)
    state__name = serializers.CharField(source='state.name' ,read_only=True)
    distributor__name = serializers.CharField(source='distributor.name' ,read_only=True)
    class Meta:
        model = BondUser
        fields = ["id","full_name", "mobile", "address", "pin_code", "city__name", "state__name", "distributor__name"]
