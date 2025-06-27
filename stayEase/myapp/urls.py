from django.urls import path
from myapp import views


urlpatterns = [
    path('base/',views.base,name='base'),
    path('',views.index,name='index'),
    
    #Propety Show 
    path('property/',views.PropertyView.as_view(),name='property'),
    
    #Property Detail Show
    path('property-detail/<int:pk>/', views.propertyDetail,name='property_detail'),
    
    #Property Create Form
    path('property-create/', views.propetyCreate, name='property_create'),
    
    #Region
    path('region/',views.region,name='region'),
    
    #Delete Region
    path('delete-region/<int:pk>/',views.delete_region,name='delete_region'),
    
    #Delete City
    path('delete-city/<int:pk>/',views.delete_city,name='delete_city'),
    
    #Login User
    path('login-user/',views.login_user,name='login_user'),
    
    #logout User
    path('logou-usr/',views.logout_user,name='logout_user'),
    
    #register user
    path('register-user/',views.register_user,name='register_user'),
]