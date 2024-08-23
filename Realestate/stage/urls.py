from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('property_list', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/new/', views.create_property, name='create_property'),
    path('property/<int:pk>/buy/', views.buy_property, name='buy_property'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    path('register/seller/', views.register_seller, name='register_seller'),
    path('property/<int:pk>/purchase-confirmation/', views.purchase_confirmation, name='purchase_confirmation'),
    path('property/<int:pk>/edit-or-delete/', views.edit_or_delete_property, name='edit_or_delete_property'),
    path('property/<int:pk>/mark-as-sold/', views.mark_as_sold, name='mark_as_sold'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

