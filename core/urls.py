from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('foods/', views.food_list, name='food_list'),
    path('food/<slug:slug>/', views.food_detail, name='food_detail'),
    path('food/<int:food_id>/review/', views.submit_review, name='submit_review'),
    path('presentation/', views.presentation, name='presentation'),
]
