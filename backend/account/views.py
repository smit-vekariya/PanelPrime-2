from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import logging
from rest_framework.views import APIView, View
from account.serializers import BondUserSerializers, BondUserListSerializers
from account.models import BondUser
from django.contrib.auth import authenticate
from django.core.cache import cache
from account.backends import AdminLoginBackend
from manager import manager
from manager.manager import HttpsAppResponse
from django.shortcuts import render
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth.models import update_last_login
from account.models import MainMenu,UserToken
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action
from manager.models import GroupPermission
from django.urls import reverse
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
            print("user_data", user_data)
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
            token['email'] = user.email
            token['full_name'] = f"{user.first_name} {user.last_name}"
            access_token =  str(token.access_token)
            refresh_token = str(token)
            UserToken.objects.update_or_create(user_id=user.id,defaults={'access_token': access_token})
            update_last_login(None, user)
            response=[{"access":str(access_token),"refresh":refresh_token}]
            return response
        except Exception as e:
            logging.exception("Something went wrong.")
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
            email = request.data["email"]
            password = request.data["password"]
            if email and password:
                user = AdminLoginBackend.authenticate(request, email=email, password=password)
                if user:
                    tokens = MyTokenObtainPairSerializer.get_token(user)
                    return HttpsAppResponse.send(tokens, 1, "Login successfully")
                else:
                    return HttpsAppResponse.send([], 0, "User is not found with this credential.")
            else:
                return HttpsAppResponse.send([], 0, "Email and password is require.")
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
