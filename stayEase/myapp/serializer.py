from rest_framework import serializers
from .models import User, CustomerProfile, AgencyProfile, OwnerProfile, Property, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'created_at', 'updated_at']

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'customer_name', 'date_of_birth', 'profile_photo', 'address']

class AgencyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyProfile
        fields = ['id', 'user', 'agency_name', 'contact_person', 'license_number', 'address', 'website', 'agency_logo']

class OwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerProfile
        fields = ['id', 'user', 'owner_name', 'address', 'owner_photo']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'name', 'property_type', 'description', 'beds', 'baths', 'has_wifi', 
                  'has_pool', 'has_kitchen', 'area_sqft', 'rent_type', 'rent_amount', 
                  'security_deposit', 'region', 'city', 'address', 'latitude', 'longitude', 
                  'status', 'is_featured', 'posted_by', 'created_at', 'updated_at', 'is_active']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'property', 'user', 'rating', 'comment', 'created_at', 'is_approved']
