from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:pk>/update_status/', views.update_ticket_status, name='update_ticket_status'),
]