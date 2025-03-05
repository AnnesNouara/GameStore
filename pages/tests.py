from django.test import TestCase
from django.urls import reverse
from .models import Category, Product
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create (
            name="Action"
        )
        self.product = Product.objects.create(
            name = "Dishonored 2",
            description = "Goated game",
            category = self.category,
            price = 15.00,
            stock = 5
        )
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Dishonored 2')
        self.assertEqual(self.product.description, 'Goated game')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, 15.00)
        
    def test_str_method_product(self):
        self.assertEqual(str(self.product), 'Dishonored 2')
        
    def test_product_get_absolute_url(self):
        expected_url = reverse('pages:product_detail', args=[self.category.id, self.product.id])
        self.assertEqual(self.product.get_absolute_url(),expected_url)
    
class ShopViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="test",password="123456")
        self.client.login(username='test', password='123456')
        
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name = 'Test',
            description = 'TestDesc',
            category = self.category,
            price = 49.99,
            stock = 5,
            available = True,
            picture = SimpleUploadedFile(name="test",content=b"",content_type='media/covers/Use_Case.jpg')
        )
    
    def test_product_detail_view(self):
        response = self.client.get(reverse('pages:product_detail',args=[self.category.id, self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertTemplateUsed(response, 'shop/product.html')
        
    def test_product_list(self):
        response = self.client.get(reverse('pages:all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
        self.assertTemplateUsed(response, 'shop/home.html')
        
class ShopUrlTestCase(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test Product",
            description = 'TestDesc',
            category = self.category,
            price = 1.99,
            stock = 5
            )
    
    def test_home_url(self):
        url = reverse('pages:all_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_detail_url(self):
        url = reverse('pages:product_detail', args=[self.category.id, self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

# Create your tests here.
