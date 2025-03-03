from django.urls import path
from .views import GameCreateView, HomePageView
from . import views

app_name = 'pages'

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
]
