from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='delivery_dashboard'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('update-status/<int:order_id>/', views.update_status, name='update_order_status'),
]
