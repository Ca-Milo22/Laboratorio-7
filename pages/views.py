from django.shortcuts import render
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