from django.urls import path, include
from .import views

urlpatterns = [
    path('', include('products.urls')),
    path('store/', views.store, name='store'),
    path('search/', views.search, name='search'),
]
