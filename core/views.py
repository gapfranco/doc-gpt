from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from core.forms import DocumentForm, LoginForm, RegisterForm, TopicForm
from core.models import Document, Topic, User


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


def _doc_context(request, topic_id):
    the_topic = Topic.objects.get(pk=topic_id)
    documents = Document.objects.filter(topic=the_topic)
    paginator = Paginator(documents, 10)
    page_doc = request.GET.get("docpage")
    doc_pages = paginator.get_page(page_doc)
    return {
        "topic": the_topic,
        "doc_pages": doc_pages,
    }


@login_required
def topic(request, topic_id):
    context = _doc_context(request, topic_id)

    return render(request, "topic.html", context)


@login_required
def document(request, topic_id):
    context = _doc_context(request, topic_id)

    return render(request, "documents.html", context)


@login_required
def new_document(request, topic_id):
    if request.method == "POST":
        the_topic = Topic.objects.get(pk=topic_id)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Document(
                name=request.POST["name"],
                topic=the_topic,
                file=request.FILES["file"],
            )
            doc.save()
    context = _doc_context(request, topic_id)
    return render(request, "documents.html", context)
