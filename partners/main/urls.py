from . import views
from django.urls import path
app_name = 'main'

urlpatterns = [
    path("", views.slash, name='slash'),
    path('ind/', views.home, name='home'),
    path('login/', views.acc_login, name='login'),
    path('logout/', views.acc_logout, name='logout'),
    path('partnerships/', views.partnerships, name='partnerships'),
    path('targets/', views.targets, name='targets'),
    path('add-partnership/', views.add_partnership, name='add_partnership'),
    path('add-target/', views.add_target, name='add_target'),
    path('delete-partnership/<int:id>/', views.delete_partnership, name='delete_partnership'),
    path('delete-target/<int:id>/', views.delete_target, name='delete_target'),
    path('all-church-partnerships/', views.church_partnerships, name='church_partners'),
    path('all-church-targets/', views.church_targets, name='church_targets'),
    path('church/', views.home_church, name='home_church'),
]