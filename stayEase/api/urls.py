from django.urls import path
from api.views import (
    CustomUserViewSet,
    CustomerProfileViewSet,
    AgencyProfileViewSet,
    RegionViewSet,
    CityViewSet,
    PropertyViewSet,
    ReviewViewSet,
    SavePropertyViewSet,
    InquiryViewSet,
    
)

property_list = PropertyViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

property_detail = PropertyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    
    #Property
    path('properties/', property_list, name='property-list'),
    path('properties/<int:pk>/', property_detail, name='property-detail'),

    # CustomUser
    path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),

    # CustomerProfile
    path('customers/', CustomerProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='customer-list'),
    path('customers/<int:pk>/', CustomerProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='customer-detail'),

    # AgencyProfile
    path('agencies/', AgencyProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='agency-list'),
    path('agencies/<int:pk>/', AgencyProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='agency-detail'),

    
    # Region
    path('regions/', RegionViewSet.as_view({'get': 'list', 'post': 'create'}), name='region-list'),
    path('regions/<int:pk>/', RegionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='region-detail'),

    # City
    path('cities/', CityViewSet.as_view({'get': 'list', 'post': 'create'}), name='city-list'),
    path('cities/<int:pk>/', CityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='city-detail'),

    # Property
    path('property/', PropertyViewSet.as_view({'get': 'list', 'post': 'create'}), name='property-list'),
    path('property/<int:pk>/', PropertyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='property-detail'),

    # Review
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-detail'),

    # SaveProperty
    path('saved-properties/', SavePropertyViewSet.as_view({'get': 'list', 'post': 'create'}), name='saveproperty-list'),
    path('saved-properties/<int:pk>/', SavePropertyViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='saveproperty-detail'),

    # Inquiry
    path('inquiries/', InquiryViewSet.as_view({'get': 'list', 'post': 'create'}), name='inquiry-list'),
    path('inquiries/<int:pk>/', InquiryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='inquiry-detail'),
]
