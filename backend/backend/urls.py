"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler400 = "manager.manager.bad_request"
handler403 = "manager.manager.permission_denied"
handler404 = "manager.manager.page_not_found"
handler500 = "manager.manager.server_error_view"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("app.urls", namespace="welcome_app")),
    path('account/',include("account.urls", namespace="account")),
    path('manager/',include("manager.urls", namespace="manager")),
    path('qr_admin/',include("qradmin.urls", namespace="qr_admin")),
    path('qr_app/',include("qrapp.urls", namespace="qr_app")),
    path('post_office/',include("postoffice.urls", namespace="post_office")),
    path('ai/',include("ai.urls", namespace="ai")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
