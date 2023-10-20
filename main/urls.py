from . import views
from django.urls import path
app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.acc_login, name='login'),
    path('logout/', views.acc_logout, name='logout'),
]