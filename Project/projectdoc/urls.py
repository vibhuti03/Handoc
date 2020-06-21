from django.contrib import admin
from django.contrib.auth import login
from django.urls import path
from doc import views
from django.contrib.auth.views import LoginView
app_name="doc"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name='home'),
    path("register/",views.register,name='register'),
    path("register/home/",views.home,name='homereg'),
    path("login/home/",views.home,name='homelog'),
    path("logout/", views.logout_request, name="logout"),
    path("login/",views.login_request,name='login'),
    path("document/",views.docform,name='document'),
    path("viewdoc/",views.viewdoc,name="viewdoc"),
    ]