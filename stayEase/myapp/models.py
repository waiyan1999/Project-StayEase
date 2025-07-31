from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('CUSTOMER', 'Customer'),
        ('AGENCY', 'Agency'),
        ('OWNER', 'Property Owner'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    customer_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='customer_profiles/', blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f'Customer: {self.customer_name}'

class AgencyProfile(models.Model):
    
    LICENSE_STATUS = [
        ('PENDING','Pending'),
        ('APPROVED','Approved'),
        ('REJECT','Reject'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agency_profile')
    agency_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, blank=True)
    license_status = models.CharField(max_length=20,choices=LICENSE_STATUS,default='PENDING')
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    agency_logo = models.ImageField(upload_to='agency_logos/', blank=True)
    
    def __str__(self):
        return f'Agency: {self.agency_name}'

class OwnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='owner_profile')
    owner_name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    owner_photo = models.ImageField(upload_to='owner_profiles/', blank=True)
    
    def __str__(self):
        return f'Owner: {self.owner_name}'

class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f'{self.name} Region'

class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = 'Cities'
        unique_together = ('region', 'name')
    
    def __str__(self):
        return f'{self.name}, {self.region.name}'

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('HOUSE', 'House'),
        ('APARTMENT', 'Apartment'),
        ('CONDO', 'Condominium'),
        ('HOSTEL', 'Hostel Room'),
    ]

    RENT_TYPE_CHOICES = [
        ('MONTH', 'Per Month'),
        ('WEEK', 'Per Week'),
        ('DAY', 'Per Day'),
        ('YEAR', 'Per Year'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('BOOKED', 'Booked'),
        ('RENTED', 'Rented'),
        ('MAINTENANCE', 'Under Maintenance'),
    ]

    ADMIN_APPROVE = [
        ('APPROVED', 'Approved'),
        ('PENDING', 'Pending'),
        ('REJECT', 'Reject'),
    ]

    name = models.CharField(max_length=100)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    description = models.TextField()

    # Amenities
    beds = models.PositiveIntegerField()
    baths = models.PositiveIntegerField()
    has_wifi = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)
    area_sqft = models.PositiveIntegerField(null=True, blank=True)

    rent_type = models.CharField(max_length=20, choices=RENT_TYPE_CHOICES)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    # Image
    primary_image = models.ImageField(upload_to='property_images/')
    image_caption = models.CharField(max_length=255, blank=True, null=True)

    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    is_featured = models.BooleanField(default=False)
    posted_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='properties')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    admin_approved = models.CharField(max_length=20, choices=ADMIN_APPROVE, default='PENDING')

    def __str__(self):
        return f'{self.name} ({self.get_property_type_display()}) in {self.city or "Unknown"}'



class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('property', 'user')
    
    def __str__(self):
        return f'{self.rating}★ review for {self.property.name}'
    
class SaveProperty(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    
class Inquiry(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sent_inquiries')
    agency_owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='received_inquiries' )
    property = models.ForeignKey(Property,on_delete=models.CASCADE,related_name='inquiries')
    message = models.CharField(max_length=255, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_replied = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Inquiry from {self.customer.username} to {self.agency_owner.username}"

    def approve(self):
        self.is_approved = True
        self.save()
        self.property.status = 'BOOKED'  # or your appropriate status
        self.property.save()
        

class ContactMessage(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,blank=True,null=True)
    sender_email = models.EmailField(blank=True,null=True)
    sender_phone = models.CharField(max_length=12,blank=True,null=True)
    sender_subject = models.CharField(max_length=15,blank=True,null=True)
    sender_message = models.TextField()
    
    def __str__(self):
        return self.sender.username
    
    