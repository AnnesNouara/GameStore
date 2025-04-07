from django.db import models
from pages.models import Product


class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Wishlist'
        ordering = ['date_added']

    def __str__(self):
        return self.wishlist_id
    
class WishListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'WishListItem'

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product
