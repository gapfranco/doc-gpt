from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.forms import LoginForm, RegisterForm, TopicForm
from core.models import Topic, User


@login_required
def frontpage(request):
    my_topics = Topic.objects.filter(user=request.user)
    return render(request, "index.html", {"my_topics": my_topics})


def login(request):
    next_url = "/"
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                form.add_error(None, "Invalid username or password")

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "next": next_url})


def register(request):
    next_url = "/"
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("name")
            password = form.cleaned_data.get("password")
            password2 = form.cleaned_data.get("password2")
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Usuário já existe")
            elif len(password) < 8:
                form.add_error(
                    "password", "Senha deve ter pelo menos 8 caracteres"
                )
            elif password2 != password:
                form.add_error("password2", "Senhas não batem")
            else:
                user = User.objects.create_user(
                    name=name, password=password, email=email
                )
                user.save()
                auth.login(request, user)
                return redirect(next_url)
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form, "next": next_url})


def signout(request):
    logout(request)
    return redirect("/")


@login_required
def new_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            user = request.user
            topic = Topic(name=name, description=description, user=user)
            topic.save()
    else:
        form = TopicForm()
    return render(request, "new_topic.html", {"form": form})


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    return render(request, "topic.html", {"topic": topic})
