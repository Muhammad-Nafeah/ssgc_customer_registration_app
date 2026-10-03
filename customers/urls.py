from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_create, name='customer_create'),
    path('<str:pk>/', views.customer_detail, name='customer_detail'),
    path('<str:pk>/edit/', views.customer_update, name='customer_update'),
    path('<str:pk>/delete/', views.customer_delete, name='customer_delete'),
]