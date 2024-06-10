from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('reset/', views.reset_password, name='reset'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('admin/', views.login_admin, name='library-admin'),
    path('', views.new, name='new'),
]