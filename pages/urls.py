from django.urls import path
from .views import GameCreateView
from . import views

app_name = 'pages'

urlpatterns = [
    path('',views.prod_list, name='home'),
    path('<uuid:category_id>/', views.prod_list, name = 'products_by_category'),
    path('<uuid:category_id>/<uuid:product_id>/', views.product_detail, name = 'product_detail'),
    path('new/', GameCreateView.as_view(), name = 'game_create'),
]
