from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.forms import SignInForm


@login_required
def frontpage(request):
    return render(request, "index.html")


def signin(request):
    next_url = "/"
    if request.method == "POST":
        form = SignInForm(request.POST)
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
        form = SignInForm()
    return render(request, "signin.html", {"form": form, "next": next_url})


def signout(request):
    logout(request)
    return redirect("/")
