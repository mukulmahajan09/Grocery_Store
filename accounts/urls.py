from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name="sign-in"),
    path('sign-up/', views.sign_up, name="sign-up"),
    path('logout/', views.logoutUser, name="logout"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_Password/', views.reset_password, name='reset_password'),
    #path('change_password/', views.change_password, name='change_password'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
]
