from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display=['email', 'username', 'age', 'is_staff']
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age",)}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields":("username","email","age","password1","password2")
            }
        )
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
# Register your models here.
