from .models import Category, Product, Developer, Rental, Review
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from .forms import RentalForm, ReviewForm


def rent_game(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            rental.product = product
            rental.save()
            return redirect('pages:rental_success')
    else:
        form = RentalForm()

    return render(request, 'rent_game.html', {'form': form, 'product': product})


def rental_success(request):
    return render(request, 'rental_success.html')

def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user)
    
    return render(request, 'my_rentals.html', {'rentals': rentals})


# Create your views here.

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()
    
class GameCreateView(ManagerRequiredMixin, CreateView):
    model = Product
    fields = ('name', 'category', 'developer', 'picture','age_rating', 'price', 'stock', 'description')
    template_name = 'shop/new_product.html'
    success_url = reverse_lazy('pages:all_products')

class GameEditView(ManagerRequiredMixin,UpdateView):
    model = Product
    fields = ('name', 'category', 'developer', 'picture','age_rating', 'price', 'stock', 'description')
    template_name = 'shop/edit_product.html'
    
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['product_id'])

class GameDeleteView(ManagerRequiredMixin,DeleteView):
    model = Product
    template_name = 'shop/delete_product.html'
    success_url = reverse_lazy('pages:all_products')
    
    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['product_id'])
    
def home_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available = True)
        
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available = True)
    
    
    if request.user.is_authenticated:
        user = request.user
        products = products.filter(developer=user.profile.Developer) | products.filter(category=user.profile.Category)
    
        products = products.filter(age_rating__lte=request.user.age)    
    
    paginator = Paginator(products, 4)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)
        
    return render(request, 'shop/home.html',{'category':category, 'prods':products})


def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available = True)
        
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available = True)
    
    paginator = Paginator(products, 8)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)
        
    return render(request, 'shop/all_products.html',{'category':category, 'prods':products})


def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    reviews = product.reviews.all()
    user_review = None

    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(product=product, user=request.user)
        except Review.DoesNotExist:
            user_review = None

    form = ReviewForm(instance=user_review) 

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = ReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('pages:product_detail',category_id=product.category_id, product_id=product_id)

    return render(request, 'shop/product.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })
                                                
def filter_view(request):
    qs = Product.objects.all()
    categories = Category.objects.all()
    developers = Developer.objects.all()
    title_contains_query = request.GET.get('title_contains','')
    price_count_min = request.GET.get('price_min','')
    price_count_max = request.GET.get('price_max','')
    age_min = request.GET.get('min_age','')
    age_max = request.GET.get('max_age','')
    reviewed = request.GET.get('reviewed','')
    category = request.GET.get('category','')
    developer = request.GET.get('developer','')
    

    if title_contains_query != '' and title_contains_query is not None:
        qs = qs.filter(name__icontains=title_contains_query)
    
    if  price_count_min != '' and price_count_min is not None:
        qs = qs.filter(price__gte=price_count_min) 
    
    if  price_count_max != '' and price_count_max is not None:
        qs = qs.filter(price__lte=price_count_max) 
    
    if age_min != '' and age_min is not None:
        qs = qs.filter(age_rating__gte=age_min)
        
    if age_max != '' and age_max is not None:
        qs = qs.filter(age_rating__lte=age_max)
        
    if category != '' and category is not None:
        qs = qs.filter(category__name=category)
    
    if developer != '' and developer is not None:
        qs = qs.filter(developer__name=developer)
    
    if reviewed == 'on':
        qs = qs.filter(id__in=Review.objects.filter(rating__gt=0).values('product_id'))
    
    context = {
        'queryset':qs,
        'categories':categories,
        'developers':developers
    }

    return render(request, 'filter.html', context)

def preorder_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available = True)
        
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, available = True)
    
    if request.user.is_authenticated:
        products = products.filter(preorder=True)
    
        products = products.filter(age_rating__lte=request.user.age)    
        
    paginator = Paginator(products, 8)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)
        
    return render(request, 'shop/preorders.html',{'category':category, 'prods':products})