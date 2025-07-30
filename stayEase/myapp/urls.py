from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index, name='index'),
    path('property/',views.PropertyView.as_view(), name='property'),
    path('property-detail/<int:pk>/',views.PropertyDetailView.as_view(),name='property_detail'),
    
    path('agency/',views.AgencyView.as_view(),name='agency'),
    path('agency-detail/<int:pk>/',views.AgencyDetailView.as_view(),name='agency_detail'),
    
    path('owner/',views.OwnerView.as_view(),name='owner'),
    path('onwer-detail/<int:pk>/',views.OwnerDetailview.as_view(),name='owner_detail'),
    
    path('location/',views.LocationView.as_view(),name='location'),
    
    #path('service/',views.ServiceView.as_view(),name='service'),
    
    path('login-user/',views.login_user, name='login_user'),
    
    path('logout-user/',views.logout_user,name='logout_user'),
    
    path('register-user/', views.register_user,name='register_user'),
    
    path('porfile/',views.ProfileView.as_view(),name='profile'),
    
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashobard'),

    path('save-property/<int:pk>/',views.SavePropertyView.as_view(),name='save_property'),
    
    path('send-inquiry/<int:pk>/',views.sendInquiry,name='send_inquiry'),
    
    path('cancel-inquiry/<int:pk>/',views.cancelInquiry,name='cancel_inquiry'),
    
    path('inquiry-detail/<int:pk>/',views.inquiryDetail,name='inquiry_detail'),
    
    path('approve-inquiry/<int:pk>/',views.approveInquiry,name='approve_inquiry'),
    
    path('reject-inquiry/<int:pk>/',views.rejectInquiry,name='reject_inquiry'),
    
    path('agency-dashboard/',views.agencyDashboard,name='agency_dashboard'),
    
    path('service/',views.service,name='service'),
    
    path('about/',views.about,name='about'),
    
    path('contact/',views.contact,name='contact'),
    
    path('agency-setting/',views.agencySetting,name='agency_setting'),
    
    path('payment/<int:pk>/', views.payment, name='payment'),

    
    
]   