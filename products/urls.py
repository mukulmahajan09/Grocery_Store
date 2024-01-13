from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_display, name='home'),
    path('category/<slug:category_slug>/', views.product_display, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_detail'),
    path('review/<int:product_id>/', views.review, name='review'),
]
