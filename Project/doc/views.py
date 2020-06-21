from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

from doc.models import LoggedUser
from .models import Post
from .forms import HomeForm


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            return redirect("home")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = UserCreationForm
    return render(request, "register.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged Out Successfully !")
    return redirect("home")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "login.html",
                  {"form": form})


def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=user_id_list)


def document(request):
    logged_users = [user.user for user in LoggedUser.objects.all()]

    return render(request, 'document.html', {"log": logged_users}, )


def docform(request):
    if request.method == "POST":
        form=HomeForm(request.POST)
        text=""
        if form.is_valid():
            Document=form.save(commit=False)
            Title = form.save(commit=False)
            Document.user=request.user
            Document.save()
            Title.save()
            text=form.cleaned_data['Document']
            form=HomeForm
            messages.info(request, "Document Saved !")
            return redirect('document')
        args={'form':form,'text': text}

        return render(request, 'document.html', args)
    if request.method=="GET":
        form = HomeForm()
        return render(request, 'document.html', {"form": form})

def viewdoc(request):
    logged_users = [user.user for user in LoggedUser.objects.all()]
    if request.method == "GET":
        posts=Post.objects.all()
    return render(request, 'viewdoc.html', {"log": logged_users,"posts":posts},)

