
from django.urls import path, include
from .views import *
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


app_name = "account"

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('main_menu/', MainMenuView.as_view(), name="main_menu"),

    # bondclick api
    path("registration/", RegisterBondUser.as_view(), name="register_bond_user"),
    path("verify_register/", VerifyRegisterUser.as_view(), name="register_verify"),
    path("login/", LoginBondUser.as_view(), name="login_bond_user"),
    path("verify_login/", VerifyLoginBondUser.as_view(), name="verify_login"),
    path("logout/", LogoutBondUser.as_view(), name="logout"),
    path('bond_user_profile/', BondUserProfile.as_view(), name="bond_user_profile"),

    # app login
    path('app_registration/', AppRegistration.as_view(), name="app-registration"),
    path('app_login/', AppLogin.as_view(), name="app-login"),
    path('app_logout/', AppLogout.as_view(), name="app-logout"),

    # cache data apis
    path('city_state_distributer/', GetCityStateDistributer.as_view(), name="city_state_distributer"),

    #adminpanel api
    path('admin_login/', AdminLogin.as_view(), name='admin_login'),
    path('user_profile/', UserProfile.as_view({'get': 'retrieve'}), name="user_profile"),
    path('edit_profile/<int:pk>', UserProfile.as_view({'get': 'put'}), name="edit_profile")


]