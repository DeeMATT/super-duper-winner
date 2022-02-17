from django.urls import path

from .views import PageListView, PageDetailView


urlpatterns = [
    path('pages/', PageListView.as_view()),
    path('pages/<slug:slug>/', PageDetailView.as_view()),
]