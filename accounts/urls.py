from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/done/', views.RegisterDoneView.as_view(), name='register_done'),
    path('pending/', views.PendingView.as_view(), name='pending'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('password/forgot/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
