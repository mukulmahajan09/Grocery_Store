"""
URL configuration for Grocery_Store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('kroger_secure_sign_in/', admin.site.urls),
    path('', include('store_app.urls')),
    path('users_accounts/', include('accounts.urls')), # user model
    path('accounts/', include('allauth.urls')), # google default dont change
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),

    #path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
    #     name="reset_password"),
#
    #path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
    #     name="password_reset_done"),
#
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
    #     name="password_reset_confirm"),
#
    #path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
    #     name="password_reset_complete"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# 1 - User submits email for reset              //PasswordResetView.as_view()           //name="reset_password"
# 2 - Email sent message                        //PasswordResetDoneView.as_view()        //name="passsword_reset_done"
# 3 - Email with link and reset instructions    //PasswordResetConfirmView()            //name="password_reset_confirm"
# 4 - Password successfully reset message       //PasswordResetCompleteView.as_view()   //name="password_reset_
