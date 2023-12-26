from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_home, name="store_home"),
    path('sign-in/', views.sign_in, name="sign-in"),
    path('sign-up/', views.sign_up, name="sign-up"),
    path('logout/', views.logoutUser, name="logout"),
]
