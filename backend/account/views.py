from django.http import HttpResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json
import logging
from rest_framework.views import APIView, View
from account.serializers import BondUserSerializers, BondUserListSerializers
from datetime import datetime, timedelta
from account.models import BondUser
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db import transaction
from account.backends import AdminLoginBackend
from manager import manager
from manager.manager import HttpsAppResponse, Util
from django.db.models import CharField, Value, F
from django.shortcuts import render
from django.db.models.functions import Concat
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from account.models import MainMenu,UserToken, City, State, Distributor, AuthOTP
from rest_framework import viewsets
from django.utils import timezone
from django.conf import settings
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from django.contrib.auth.models import Group
from manager.models import GroupPermission
from django.urls import reverse
from postoffice.views import send_otp_to_mobile
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from manager.manager import create_from_exception
from django.shortcuts  import redirect
from django.contrib.auth import login, authenticate, logout


# Create your views here.

class UserProfile(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            user_id = request.user.id
            user_data = BondUserListSerializers(BondUser.objects.filter(id=user_id), many=True).data
            return HttpsAppResponse.send([user_data], 1, "User Profile data get successfully.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))

    def put(self, request, pk=None):
        try:
            serializer = BondUserListSerializers(BondUser.objects.get(pk=pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return HttpsAppResponse.send([], 1, "User Profile Updated.")
            else:
                error_messages = ", ".join(value[0] for key, value in serializer.errors.items())
                return HttpsAppResponse.send([], 0, error_messages)
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        try:
            token = super().get_token(user)
            token['mobile'] = user.mobile
            token['full_name'] = user.full_name
            access_token =  str(token.access_token)
            refresh_token = str(token)
            UserToken.objects.update_or_create(user_id=user.id,defaults={'access_token': access_token})
            update_last_login(None, user)
            response=[{"access":str(access_token),"refresh":refresh_token}]
            return response
        except Exception as e:
            manager.create_from_exception(e)

class AppLogin(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/login.html"
    success_url = "app:ask-anything-page"
    redirect_field_name = 'next' 

    def get(self, request, *args, **kwargs):
        return Response(status=200, template_name=self.template_name)
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user = authenticate(request, username=data["mobile"], password=data["password"])
            if user is not None:
                login(request, user , backend='django.contrib.auth.backends.ModelBackend')                
            redirect_to = request.GET.get(self.redirect_field_name, None)
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect(reverse(self.success_url))
        except Exception as e:
            logging.exception("Something went wrong.")
            create_from_exception(e)
            return render(request, self.template_name, context={"msg":str(e)})

          
class AppLogout(APIView):
    authentication_classes = []
    permission_classes = []
    success_url = "app:welcome-page"
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse(self.success_url))
    
    
class AppRegistration(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "app/registration.html"
    success_url = "/account/app_login/"

    def get(self, request, *args, **kwargs):
        return Response(status=200, template_name=self.template_name)

    def post(self ,request, *args, **kwargs):
        try:
            data = request.data
            if data["password"] != data["confirm_password"]:
                raise Exception("Confirm password does not match.")
            password = make_password(data["confirm_password"])
            serializer = BondUserSerializers(data={"full_name":data["full_name"],"mobile":data["mobile"],"email":data["email"],"password":password,"is_app_user":True})
            if serializer.is_valid():
                serializer.save()
            else:
                error_messages = ", ".join(value[0] for key, value in serializer.errors.items())
                raise Exception(error_messages)
            return redirect(self.success_url)
        except Exception as e:
            logging.exception("Something went wrong.")
            create_from_exception(e)
            return render(request, self.template_name, context={"msg":str(e)})

class AppLogout(APIView):
    authentication_classes =[]
    permission_classes = []
    success_url = "/account/app_login/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.success_url)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AdminLogin(APIView):
    authentication_classes =[]
    permission_classes = []
    def post(self,request):
        try:
            mobile = request.data["mobile"]
            password = request.data["password"]
            if mobile and password:
                user = AdminLoginBackend.authenticate(request, mobile=mobile, password=password)
                if user:
                    tokens = MyTokenObtainPairSerializer.get_token(user)
                    return HttpsAppResponse.send(tokens, 1, "Login successfully")
                else:
                    return HttpsAppResponse.send([], 0, "User is not found with this credential.")
            else:
                return HttpsAppResponse.send([], 0, "Mobile and password is require.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class MainMenuView(APIView):
    def get(self, request):
        try:
            if request.user.is_superuser is False:
                can_view_page = GroupPermission.objects.select_related('permissions').filter(group=request.user.groups.id,has_perm=True,permissions__act_code='can_view').values_list("permissions__page_name_id", flat=True)
                menu = list(MainMenu.objects.filter(id__in=can_view_page).values().order_by("sequence"))
            else:
                menu = list(MainMenu.objects.values().order_by("sequence"))
            return HttpsAppResponse.send(menu, 1, "Get Main Menu data successfully.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))



class RegisterUser(APIView):
    authentication_classes =[]
    permission_classes = []
    def post(self, request):
        try:
            serializer = BondUserSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return HttpsAppResponse.send([], 1, "Registration successfully")
            else:
                error_messages = ", ".join(value[0] for key, value in serializer.errors.items())
                return HttpsAppResponse.send([], 0, error_messages)
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class RegisterBondUser(APIView):
    authentication_classes =[]
    permission_classes = []
    def post(self, request):
        try:
            register_user_data = request.data
            mobile_no = register_user_data["mobile"]
            if not mobile_no:
                return HttpsAppResponse.send([], 0, "Mobile number is required.")
            if BondUser.objects.filter(mobile=mobile_no).exists():
                return HttpsAppResponse.send([], 0, "Mobile number is already registered.")
            if not City.objects.filter(id=register_user_data["city"],state=register_user_data["state"]).exists():
                return HttpsAppResponse.send([], 0, "City is not available in selected state.")
            serializer = BondUserSerializers(data=register_user_data)
            if not serializer.is_valid():
                error_messages = ", ".join(value[0] for key, value in serializer.errors.items())
                return HttpsAppResponse.send([], 0, error_messages)
            otp = send_otp_to_mobile(mobile_no)
            if len(str(otp)) > 6:
                return HttpsAppResponse.send([], 0, otp)
            register_user_data["mobile"] = mobile_no
            AuthOTP.objects.update_or_create(key=f"register_{mobile_no}",defaults={"otp":otp,"created_on":timezone.now(),"value":json.dumps(register_user_data),"is_used":False})
            return HttpsAppResponse.send([], 1, "Otp has been send to mobile number successfully")
        except Exception as e:
           return HttpsAppResponse.exception(str(e))


class VerifyRegisterUser(APIView):
    authentication_classes =[]
    permission_classes = []
    def post(self,request):
        try:
            verify_data = request.data
            user_data = AuthOTP.objects.filter(key=f"register_{verify_data['mobile']}",is_used=False).first()
            if user_data:
                if str(user_data.otp) != str(verify_data["otp"]):
                    return HttpsAppResponse.send([], 0, "OTP verification failed. Please make sure you have entered the correct OTP.")
                if user_data.expire_on > timezone.now():
                    data = json.loads(user_data.value)
                    data["company"] = int(settings.DEFAULT_COMPANY_ID)
                    serializer = BondUserSerializers(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        user_data.is_used = True
                        user_data.save()
                        user = authenticate(request, mobile=data["mobile"])
                        tokens = MyTokenObtainPairSerializer.get_token(user)
                        return HttpsAppResponse.send(tokens, 1, "Registration successfully")
                    else:
                        error_messages = ", ".join(value[0] for key, value in serializer.errors.items())
                        return HttpsAppResponse.send([], 0, error_messages)
                else:
                    return HttpsAppResponse.send([], 0, "Your OTP has expired. Please request a new OTP.")
            return HttpsAppResponse.send([], 0, "You need to register your self.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class LoginBondUser(APIView):
    authentication_classes =[]
    permission_classes = []
    def post(self,request):
        try:
            login_data = request.data
            mobile_no = login_data["mobile"]
            is_exit=  BondUser.objects.filter(mobile=mobile_no).exists()
            if is_exit:
                otp = send_otp_to_mobile(mobile_no)
                if len(str(otp)) > 6:
                    return HttpsAppResponse.send([], 0, otp)
                login_data["mobile"] = mobile_no
                AuthOTP.objects.update_or_create(key=f"login_{mobile_no}",defaults={"otp":otp,"created_on":timezone.now(),"value":json.dumps(login_data),"is_used":False})
                return HttpsAppResponse.send([], 1, "Otp has been send to mobile number successfully")
            else:
                return HttpsAppResponse.send([], 0, "User not found.")
        except Exception as e:
           return HttpsAppResponse.exception(str(e))


class VerifyLoginBondUser(APIView):
    authentication_classes =[]
    permission_classes = []
    def post(self,request):
        try:
            login_data = request.data
            user_data = AuthOTP.objects.filter(key=f"login_{login_data['mobile']}", is_used=False).first()
            if user_data:
                if str(user_data.otp) != str(login_data["otp"]):
                    return HttpsAppResponse.send([], 0, "OTP verification failed. Please make sure you have entered the correct OTP.")
                if user_data.expire_on > timezone.now():
                    user = authenticate(request, mobile=login_data["mobile"])
                    tokens = MyTokenObtainPairSerializer.get_token(user)
                    user_data.is_used = True
                    user_data.save()
                    return HttpsAppResponse.send(tokens, 1, "Login successfully.")
                else:
                    return HttpsAppResponse.send([], 0, "Your OTP has expired. Please request a new OTP.")
            return HttpsAppResponse.send([], 0, "You need to log in using your mobile number.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class LogoutBondUser(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            UserToken.objects.filter(user_id=request.user.id).delete()
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return HttpsAppResponse.send([], 1, "User logout successfully.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class BondUserProfile(APIView):
    def get(self, request):
        try:
            user_info = BondUser.objects.filter(id=request.user.id).values("full_name","mobile").annotate(full_address=Concat(F("address"), Value(', '), ("pin_code"), Value(', '), F("city__name"), Value(', '), F("state__name"),output_field=CharField())).first()
            return HttpsAppResponse.send([user_info], 1, "User profile details.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))



class GetCityStateDistributer(APIView):
    authentication_classes =[]
    permission_classes = []
    def get(self,request):
        try:
            city = list(City.objects.filter(is_deleted=False).values("id","name").order_by("name"))
            state = list(State.objects.filter(is_deleted=False).values("id","name").order_by("name"))
            distributor = list(Distributor.objects.filter(is_deleted=False).values("id","name").order_by("name"))
            response = [{"City":city,"State":state,"Distributor":distributor}]
            return HttpsAppResponse.send(response, 1, "City and state data fetch successfully.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


