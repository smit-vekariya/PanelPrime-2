from django.contrib import admin
from account.models import MainMenu, Company, Distributor, BondUser, State, City, UserToken, AuthOTP


# Register your models here.


@admin.register(MainMenu)
class MainMenuAdmin(admin.ModelAdmin):
    list_display = ("name","code", "url", "sequence", "parent", "is_parent", "icon")


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ('name', 'identity_id', 'company', 'is_deleted')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'identity_id', 'is_deleted')

@admin.register(BondUser)
class BondUserAdmin(admin.ModelAdmin):
    list_display = ("mobile", "full_name", "address", "city", "pin_code", "state", "created_on", "company", "distributor", "is_deleted")


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_deleted')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'state', 'is_deleted')


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "access_token", "is_allowed")


@admin.register(AuthOTP)
class AuthOTPAdmin(admin.ModelAdmin):
    list_display =('key','value', 'otp', 'expire_on', 'created_on', 'is_used')


