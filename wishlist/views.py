from django.shortcuts import redirect, render
from pages.models import Product
from django.core.exceptions import ObjectDoesNotExist
from .models import Wishlist, WishListItem

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def add_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(wishlist_id=_wishlist_id(request))
        wishlist.save()
    try:
        wishlist_item = WishListItem.objects.get(product=product, wishlist=wishlist)
        if (wishlist_item.quantity < wishlist_item.product.stock):
            wishlist_item.quantity +=1
        wishlist_item.save()
    except WishListItem.DoesNotExist:
        wishlist_item = WishListItem.objects.create(product=product, quantity=1,wishlist=wishlist)
    return redirect('wishlist:wishlist_detail')


def wishlist_detail(request, total=0, counter=0, wishlist_items = None):
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishListItem.objects.filter(wishlist=wishlist, active=True)
        for wishlist_item in wishlist_items:
            total += (wishlist_item.product.price * wishlist_item.quantity)
            counter += wishlist_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'wishlist.html',
    {'wishlist_items':wishlist_items,
    'total':total,
    'counter':counter
    })
# Create your views here.
