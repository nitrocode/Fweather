from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # html pages
    #  admin pages
    path('admin/', admin.site.urls),
    #  home page is the subscribe page
    path('', views.HomePageView.as_view(), name='subscribe'),
    #  about page
    path('about/', views.AboutPageView.as_view(), name='about'),
    # programmatic routes
    #  sign up route hit by jquery
    path('signup', views.sign_up, name='signup'),
    #  verify email route hit when clicking on the email link
    path('verify', views.verify, name='verify'),
]
