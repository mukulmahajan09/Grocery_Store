from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name="sign-in"),
    path('sign-up/', views.sign_up, name="sign-up"),
    path('logout/', views.logoutUser, name="logout"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('change_password/', views.change_password, name='change_password'),
]
