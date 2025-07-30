from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from myapp.models import *
from api.serializers import *


User = get_user_model()

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class =PropertySerializer
    
    def get_queryset(self):
        user = self.request.user
        # Only allow agency or owner to edit their own properties
        return Property.objects.filter(posted_by=user)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

class AgencyProfileViewSet(viewsets.ModelViewSet):
    queryset = AgencyProfile.objects.all()
    serializer_class = AgencyProfileSerializer

class OwnerProfileViewSet(viewsets.ModelViewSet):
    queryset = OwnerProfile.objects.all()
    serializer_class = OwnerProfileSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class SavePropertyViewSet(viewsets.ModelViewSet):
    queryset = SaveProperty.objects.all()
    serializer_class = SavePropertySerializer

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
