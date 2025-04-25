from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, View
from pages.models import Product
from django.urls import reverse_lazy, reverse
from .forms import StockUpdateForm


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

class StockEditView(ManagerRequiredMixin, UpdateView):
    model = Product
    fields = ('stock',)
    template_name= 'edit_stock.html'
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['product_id'])
    
    def get_success_url(self):
        return reverse('manager_dashboard:stock_detail', kwargs={'product_id': self.object.id})

class StockView(ManagerRequiredMixin, View):
    def get(self, request):
        prods = Product.objects.all()
        prods = prods.order_by('-sold_count')
        return render(request, 'overview.html', {'prods' : prods})
    
class StockDetail(ManagerRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'stock_detail.html', {'product' : product})
    
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['product_id'])
