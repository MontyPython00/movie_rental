from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', views.SignOutView.as_view(), name='logout')
]