from django.test import TestCase
from .models import Profile, Developer, Category
from django.contrib.auth import get_user_model
from django.urls import reverse

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'test',
            password='123456',
            age = 23
        )
    
    def test_create_user(self):
        self.assertEqual(self.user.username,'test')
        self.assertTrue(self.user.check_password('123456'))
        self.assertEqual(self.user.age,23)
    
    def test_superuser_make(self):
        self.superuser = get_user_model().objects.create_superuser(
            username='SuperTest',
            password = 'SuperPass'
        )
        self.assertEqual(self.superuser.username, 'SuperTest')
        self.assertTrue(self.superuser.check_password('SuperPass'))
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test'
        )
        Profile.objects.filter(user=self.user).delete()
        self.developer = Developer.objects.create(name='Bethesda')
        self.category = Category.objects.create(name='Action')
        
        self.profile = Profile.objects.create(
            
            user=self.user,
            date_of_birth = '2001-12-12',
            Developer = self.developer,
            Category = self.category
        )
    
    def test_profile_creation(self):
        expected_date = '2001-12-12'
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.date_of_birth, expected_date )
        self.assertEqual(self.profile.Developer, self.developer)
        self.assertEqual(self.profile.Category, self.category)
        
    def test_profile_str(self):
        expected = self.user.username
        self.assertEqual(str(self.profile),expected)
    
    def test_absolute_url(self):
        expected = reverse('user_profile', kwargs={'pk': self.profile.pk})
        self.assertEqual(self.profile.get_absolute_url(),expected)

class HomepageTests(TestCase):
        def test_homepage_status(self):
            response = self.client.get(reverse('pages:all_products'))
            self.assertEqual(response.status_code, 200)