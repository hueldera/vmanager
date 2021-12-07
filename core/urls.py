from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


frontend_view = ensure_csrf_cookie(lambda r: render(r, "index.html"))

urlpatterns = [
    path("api/", include("vulnerabilities.urls")),
    re_path(r"^(?:.*)/?$", frontend_view),
]
