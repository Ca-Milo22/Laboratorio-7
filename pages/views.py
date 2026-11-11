
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Resource


def home(request):
    resource_count = Resource.objects.count()

    return render(
        request,
        "pages/home.html",
        {"resource_count": resource_count}
    )


def resources(request):
    resources = Resource.objects.select_related("category").all()

    return render(
        request,
        "pages/resources.html",
        {"resources": resources}
    )


def available_resources(request):
    resources = Resource.objects.select_related("category").filter(
        available=True
    )

    return render(
        request,
        "pages/resources.html",
        {"resources": resources}
    )


def about(request):
    return render(request, "pages/about.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("pages:dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("pages:login")
    else:
        form = UserCreationForm()

    return render(
        request,
        "pages/signup.html",
        {"form": form}
    )


@login_required
def dashboard(request):
    visits = request.session.get("dashboard_visits", 0)
    visits += 1
    request.session["dashboard_visits"] = visits

    return render(
        request,
        "pages/dashboard.html",
        {"visits": visits}
    )


@login_required
@permission_required("pages.view_resource", raise_exception=True)
def resource_review(request):
    resources = Resource.objects.select_related("category").all()

    return render(
        request,
        "pages/review.html",
        {"resources": resources}
    )
