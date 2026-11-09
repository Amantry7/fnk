from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit_request, name='submit_request'),
    path('novosti/<slug:slug>/', views.news_detail, name='news_detail'),
]
