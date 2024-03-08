from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from markdown import markdown

from core.forms import (
    DocumentForm,
    LoginForm,
    QuestionForm,
    RegisterForm,
    TopicForm,
)
from core.models import Document, Question, Topic, User
from core.utils.QueryManager import QueryManager


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
            return redirect(f"topic/{topic.id}")
            # return render(request, "index.html")
    else:
        form = TopicForm()
    return render(request, "new_topic.html", {"form": form})


@login_required
def edit_topic(request, topic_id):
    the_topic = Topic.objects.get(id=topic_id)

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            the_topic.name = form.cleaned_data.get("name")
            the_topic.description = form.cleaned_data.get("description")
            the_topic.save()
            return redirect(f"/topic/{the_topic.id}")
    else:
        form = TopicForm(
            initial={
                "name": the_topic.name,
                "description": the_topic.description,
            }
        )

    return render(request, "new_topic.html", {"form": form})


@login_required
def delete_topic(request, topic_id):
    the_topic = Topic.objects.get(id=topic_id)
    if request.method == "POST":
        the_topic.delete()
        return redirect("/")
    return render(request, "delete_topic.html", {"topic": the_topic})


def _context(request, topic_id):
    the_topic = Topic.objects.get(pk=topic_id)
    documents = Document.objects.filter(topic=the_topic)
    paginator = Paginator(documents, 10)
    page_doc = request.GET.get("docpage")
    doc_pages = paginator.get_page(page_doc)
    questions = Question.objects.filter(topic=the_topic)
    paginator2 = Paginator(questions, 6)
    page_que = request.GET.get("qpage")
    que_pages = paginator2.get_page(page_que)
    return {
        "topic": the_topic,
        "doc_pages": doc_pages,
        "que_pages": que_pages,
    }


@login_required
def topic(request, topic_id):
    context = _context(request, topic_id)

    return render(request, "topic.html", context)


@login_required
def query(request, topic_id):
    context = _context(request, topic_id)

    return render(request, "query.html", context)


@login_required
def document(request, topic_id):
    context = _context(request, topic_id)

    return render(request, "documents.html", context)


@login_required
def question(request, topic_id):
    context = _context(request, topic_id)

    return render(request, "history.html", context)


@login_required
def qa(request, question_id):
    quest = Question.objects.get(pk=question_id)
    context = {
        "question": quest.text,
        "answer": markdown(quest.answer),
        "topic_id": quest.topic.id,
    }
    return render(request, "qa.html", context)


@login_required
def new_document(request, topic_id):
    if request.method == "POST":
        the_topic = Topic.objects.get(pk=topic_id)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Document(
                topic=the_topic,
                file=request.FILES["file"],
            )
            doc.save()
    context = _context(request, topic_id)
    return render(request, "documents.html", context)


class HttpRespoonse:
    pass


@login_required
def ask(request, topic_id):
    saida = ""
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            the_topic = Topic.objects.get(pk=topic_id)
            query_manager = QueryManager(topic_id)
            quest = form.cleaned_data.get("question")
            answer, cost = query_manager.question(quest)
            saida = answer["result"]
            Question.objects.create(
                topic=the_topic, text=quest, answer=saida, cost=cost
            )
    return HttpResponse(saida)
