from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, View
from pages.models import Product


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

class StockEditView(ManagerRequiredMixin, UpdateView):
    model = Product
    fields = ('stock')
    template_name = 'manager_dashboard/edit_stock.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['product_id'])

class StockView(ManagerRequiredMixin, View):
    def get(self, request):
        prods = Product.objects.all()
        prods = prods.order_by('-sold_count')
        return render(request, 'overview.html', {'prods' : prods})
    
