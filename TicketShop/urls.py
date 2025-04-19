from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='tickets'), path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),  
]