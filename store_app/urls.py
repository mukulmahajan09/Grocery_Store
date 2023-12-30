from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_display, name="store_home"),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_detail'),
]
