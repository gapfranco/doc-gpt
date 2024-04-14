from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from markdown import markdown

from core.forms import (
    DocumentForm,
    InviteForm,
    LoginForm,
    ProfileForm,
    QuestionForm,
    RegisterForm,
    TopicForm,
)
from core.models import (
    Document,
    DocumentBody,
    Question,
    Topic,
    TopicInvite,
    TopicInviteSent,
    User,
)
from core.utils.mail_invite import topic_invite
from core.utils.query_manager import QueryManager


def main(request):
    return render(request, "index.html")


def stripe(request):
    return render(request, "partials/stripe.html")


def empty(request):
    return HttpResponse("")


def profile(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.name = form.cleaned_data.get("name")
            user.preferred_language = form.cleaned_data.get(
                "preferred_language"
            )
            user.save()
            return redirect("/main")
    else:
        form = ProfileForm(
            {
                "name": user.name,
                "preferred_language": user.preferred_language,
                "query_balance": user.query_balance,
                "query_credits": user.query_credits,
            }
        )

    return render(request, "profile.html", {"form": form})


@login_required
def frontpage(request):
    invites = [
        invite.topic.id
        for invite in TopicInvite.objects.filter(user=request.user)
    ]
    my_topics = Topic.objects.filter(
        Q(user=request.user) | Q(publish=True) & (Q(id__in=invites))
    )

    return render(request, "main.html", {"my_topics": my_topics})


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
    next_url = "/main"
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
                create_invites(user)
                auth.login(request, user)
                return redirect(next_url)
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form, "next": next_url})


def create_invites(user):
    for invite_sent in TopicInviteSent.objects.filter(email=user.email):
        topic = invite_sent.topic
        if not TopicInvite.objects.filter(topic=topic, user=user).exists():
            invite = TopicInvite(topic=topic, user=user)
            invite.save()


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
            type = form.cleaned_data.get("type")
            user = request.user
            topic = Topic(
                name=name, description=description, type=type, user=user
            )
            topic.save()
            return redirect(f"topic/{topic.id}")
            # return render(request, "index.html")
    else:
        form = TopicForm()
    return render(request, "new_topic.html", {"form": form, "id": ""})


@login_required
def edit_topic(request, topic_id):
    the_topic = Topic.objects.get(id=topic_id)

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            the_topic.name = form.cleaned_data.get("name")
            the_topic.description = form.cleaned_data.get("description")
            the_topic.type = form.cleaned_data.get("type")
            the_topic.save()
            return redirect(f"/topic/{the_topic.id}")
    else:
        form = TopicForm(
            initial={
                "name": the_topic.name,
                "description": the_topic.description,
                "type": the_topic.type,
            }
        )

    return render(
        request, "new_topic.html", {"form": form, "id": the_topic.id}
    )


@login_required
def delete_topic(request, topic_id):
    the_topic = Topic.objects.get(id=topic_id)
    if request.method == "POST":
        the_topic.delete()
        return redirect("/main")
    return render(request, "delete_topic.html", {"topic": the_topic})


def _context(request, topic_id):
    the_topic = Topic.objects.get(pk=topic_id)
    documents = Document.objects.filter(topic=the_topic)
    paginator = Paginator(documents, 8)
    page_doc = request.GET.get("docpage")
    doc_pages = paginator.get_page(page_doc)
    questions = Question.objects.filter(topic=the_topic, user=request.user)
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

    return render(request, "partials/query.html", context)


@login_required
def chat(request, topic_id):
    context = _context(request, topic_id)

    return render(request, "partials/chat.html", context)


@login_required
def document(request, topic_id):
    context = _context(request, topic_id)

    return render(request, "partials/documents.html", context)


def _publish_context(request, topic_id):
    the_topic = Topic.objects.get(pk=topic_id)
    invites = TopicInviteSent.objects.filter(topic=the_topic)
    paginator = Paginator(invites, 8)
    page_inv = request.GET.get("invpage")
    inv_pages = paginator.get_page(page_inv)
    return {
        "topic": the_topic,
        "paginator": paginator,
        "inv_pages": inv_pages,
    }


@login_required
def publish(request, topic_id):
    context = _publish_context(request, topic_id)

    return render(request, "partials/publish.html", context)


@login_required
def publish_topic(request, topic_id):
    the_topic = Topic.objects.get(pk=topic_id)
    the_topic.publish = not the_topic.publish
    the_topic.save()
    return redirect(f"/topic/{topic_id}")
    # context = _context(request, topic_id)
    # return render(request, "partials/documents.html", context)


@login_required
def chat_detail(request, question_id):
    quest = Question.objects.get(pk=question_id)
    context = {
        "question": quest.text,
        "answer": markdown(quest.answer),
        "created_at": quest.created_at,
        "id": quest.id,
        "topic_id": quest.topic.id,
    }
    return render(request, "partials/chat_detail.html", context)


@login_required
def chat_delete(request, id):
    quest = Question.objects.get(pk=id)
    topic_id = quest.topic_id
    quest.delete()
    return redirect(f"/chat/{topic_id}")


@login_required
def new_document(request, topic_id):
    error = ""
    if request.method == "POST":
        the_topic = Topic.objects.get(pk=topic_id)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Document(
                topic=the_topic,
                base_name=request.FILES["file"].name,
            )
            file = request.FILES.get("file")
            body = b""
            for chunk in file.chunks():
                body += chunk
            doc.save()
            doc_body = DocumentBody(
                document=doc, doc=body, type=file.content_type
            )
            doc_body.save()
        else:
            error = form.errors["file"][0]
    context = _context(request, topic_id)
    context["error"] = error
    return render(request, "partials/documents.html", context)


def maybe_create_invite(email, topic):
    user = User.objects.filter(email=email).first()
    if user:
        if not TopicInvite.objects.filter(topic=topic, user=user).exists():
            invite = TopicInvite(topic=topic, user=user)
            invite.save()
    topic_invite.delay(topic.id, email)


@login_required
def new_invite(request, topic_id):
    error = ""
    if request.method == "POST":
        the_topic = Topic.objects.get(pk=topic_id)
        form = InviteForm(request.POST)
        if form.is_valid():
            invite_sent = TopicInviteSent.objects.filter(
                topic=the_topic, email=form.cleaned_data["email"]
            )
            if invite_sent.exists():
                error = "Convite já foi enviado para esse email"
            else:
                email = form.cleaned_data["email"]
                invite_sent = TopicInviteSent(topic=the_topic, email=email)
                invite_sent.save()
                maybe_create_invite(email, the_topic)
        else:
            error = form.errors["email"][0]
    context = _publish_context(request, topic_id)
    context["error"] = error
    return render(request, "partials/publish.html", context)


class HttpRespoonse:
    pass


@login_required
def ask(request, topic_id):
    context = _context(request, topic_id)
    # saida = ""
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            the_topic = Topic.objects.get(pk=topic_id)
            query_manager = QueryManager(topic_id)
            quest = form.cleaned_data.get("question")
            answer, cost = query_manager.question(quest)
            saida = answer
            quest = Question.objects.create(
                topic=the_topic,
                text=quest,
                answer=saida,
                cost=cost,
                user=request.user,
            )
            context = {
                "question": quest.text,
                "answer": markdown(quest.answer),
                "created_at": quest.created_at,
                "id": quest.id,
                "topic_id": quest.topic.id,
            }
            return render(request, "partials/chat_detail.html", context)
    return render(request, "partials/chat.html", context)


@login_required
def delete_user_account(request):
    user = request.user
    # user.is_active = False  # Opção 1: torna o usuário inativo
    # user.save()
    user.delete()  # Opção 2: Excluir o usuário diretamente
    logout(request)
    return redirect("/")


@login_required
def delete_invite(request, topic_id, invite_id):
    invite_sent = TopicInviteSent.objects.get(id=invite_id)
    user = User.objects.filter(email=invite_sent.email).first()
    if user:
        TopicInvite.objects.get(user=user, topic__id=topic_id).delete()
    invite_sent.delete()
    context = _publish_context(request, topic_id)
    return render(request, "partials/publish.html", context)


@login_required
def send_invite(request, topic_id, invite_id):
    invite_sent = TopicInviteSent.objects.get(id=invite_id)
    topic_invite.delay(topic_id, invite_sent.email)
    context = _publish_context(request, topic_id)
    return render(request, "partials/publish.html", context)


@login_required
def doc_summary(request, doc_id):
    doc = Document.objects.get(id=doc_id)
    context = {
        "document": doc,
    }
    return render(request, "partials/doc_detail.html", context)
