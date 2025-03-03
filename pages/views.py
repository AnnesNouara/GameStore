from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, UpdateView


# Create your views here.

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()
    
class GameCreateView(ManagerRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'category', 'developer', 'picture', 'price', 'stock_quantity', 'description')
    template_name = 'shop/new_product.html'
    success_url = reverse_lazy('pages:all_products')

class GameEditView(ManagerRequiredMixin,UpdateView):
    model = Product
    fields = ('name', 'category', 'developer', 'picture', 'price', 'stock_quantity', 'description')
    template_name = 'shop/edit_product.html'
    
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['product_id'])

class GameDeleteView(ManagerRequiredMixin,DeleteView):
    model = Product
    template_name = 'shop/delete_product.html'
    success_url = reverse_lazy('pages:all_products')
    
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['product_id'])

def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available = True)
        
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available = True)
    
    paginator = Paginator(products, 6)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)
        
    return render(request, 'shop/home.html',{'category':category, 'prods':products})

def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    return render(request, 'shop/product.html', {'product':product})
