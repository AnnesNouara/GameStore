from pages.models import Product;
from django.views.generic import ListView;
from django.db.models import Q;

class SearchResultListView(ListView):
    model = Product
    context_object_name = "prod_list"
    template_name = "shop/search.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query) | Q(developer__name__icontains=query))

    def get_context_data(self, **kwargs):
        context = super(SearchResultListView,self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context