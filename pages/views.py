from django.views.generic import ListView, TemplateView
from .models import Category, Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import CreateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class GameListView(ListView):
    model = Product
    template_name = 'game_list.html'
    context_object_name = 'all_games_list'

# Create your views here.

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()
    
class GameCreateView(ManagerRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'category', 'developer', 'picture', 'price', 'stock_quantity', 'description')
    template_name = 'game/new_game.html'

    def prod_list(request, category_id=None):
        category = None
        products = Product.objects.filter(available = True)
        
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            products = Product.objects.filter(category=category, available = True)
    
    #paginator to be put in

def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    return render(request, 'game/product.html', {'product':product})
