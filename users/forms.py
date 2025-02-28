from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
   class Meta:
      model = CustomUser
      fields = ('email','username', 'password1', 'password2','age' )


class CustomUserChangeForm(UserChangeForm):
     class Meta:
         model = CustomUser
         fields = UserChangeForm.Meta.fields