from django.urls import path
from .views import GameCreateView, GameDeleteView, GameEditView
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.prod_list, name = 'all_products'),
    path('<uuid:category_id>/', views.prod_list, name = 'products_by_category'),
    path('<uuid:category_id>/<uuid:product_id>/', views.product_detail, name = 'product_detail'),
    path('<uuid:category_id>/<uuid:product_id>/edit', GameEditView.as_view(), name = 'game_edit'),
    path('<uuid:category_id>/<uuid:product_id>/delete', GameDeleteView.as_view(), name = 'game_delete'),
    path('new/', GameCreateView.as_view(), name = 'game_create')
]
