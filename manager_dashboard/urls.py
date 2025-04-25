from django.urls import path
from . import views

app_name='manager_dashboard'

urlpatterns = [
    path('overview/', views.StockView.as_view() , name='overview')
]