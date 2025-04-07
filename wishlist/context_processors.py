from .models import Wishlist, WishListItem
from .views import _wishlist_id

def counter(request):
    item_count1 = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
            wishlist_items = WishListItem.objects.all().filter(wishlist=wishlist[:1])
            for wishlist_item in wishlist_items:
                item_count1 += wishlist_item.quantity
        except Wishlist.DoesNotExist:
            item_count1 = 0
    return {'item_count1':item_count1}