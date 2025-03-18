from django.urls import path
from .views import SearchResultListView

app_name = 'search_app'

urlpatterns = [
    path('',SearchResultListView.as_view(), name="searchResult"),
]