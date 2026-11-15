"""lostfound/urls.py – URL patterns (Phase 2 will add more)."""
from django.urls import path
from . import views

urlpatterns = [
    path("report/",             views.report_item, name="report_item"),
    path("found/",              views.found_list,  name="found_list"),
    path("found/<str:pk>/",     views.found_detail, name="found_detail"),
    path("matches/",            views.my_matches,  name="my_matches"),
]
