from django.urls import path
from .views import CustomerSignUpView, ManagerSignUpView, ProfileEditView, ProfilePageView

urlpatterns=[
    path('c_signup/', CustomerSignUpView.as_view(), name='csignup'),
    path('m_signup/', ManagerSignUpView.as_view(), name='msignup'),
    path('edit_profile/<int:pk>/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<int:pk>/', ProfilePageView.as_view(), name='user_profile'),
]