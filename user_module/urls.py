from django.urls import path
from user_module import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('profile/', views.ProfileView.as_view(), name='profile_page'),
    path('profile/edit-info-page/', views.EditInfoView.as_view(), name='edit_info_page'),
    path('profile/change-password', views.ChangePasswordView.as_view(), name='change_pass_page'),
    path('profile/edit-address', views.EditAddressView.as_view(), name='edit_address_page'),
    path('profile/edit-address/counties/', views.load_counties, name='edit_counties'),
    path('verification/', views.verify_password, name='verification_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('activate-account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account'),
]