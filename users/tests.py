from django.test import TestCase
from .models import Profile
from django.contrib.auth import get_user_model

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
        
# Create your tests here.
