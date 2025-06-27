from django.db import models
from django.contrib.auth.models import User


# class UserRole(models.Model):
#     class USER_ROLE(models.TextChoices):
#         AGENCY = 'agency' , 'Agency'
#         OWNER = 'owner' , 'Owner'
#         CUSTOMER = 'customer', 'Customer'
    
#     role = models.CharField(max_length=10, choices=USER_ROLE.choices,default=USER_ROLE.CUSTOMER)
    
#     def __str__(self):
#         return f'User Role - {self.role}'











#Customer Profile  
class CustomerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255,blank=True)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255,blank=True)
    date_of_birth = models.DateTimeField(null=True,blank=True)
    profile_photo = models.ImageField(upload_to='customer-profile',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Customer: {self.name}'

# Agency Profile   
class AgencyProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=11)
    license_number = models.CharField(max_length=50,blank=True)
    address = models.CharField(max_length=255,blank=True)
    website = models.URLField(blank=True)
    agency_logo = models.ImageField(upload_to='agency-logo',blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Agency: {self.agency_name}'
    

#Owern Profile
class OwnerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255,blank=True)
    owner_photo = models.ImageField(upload_to='owner-profile',blank=True)
    registered_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Owner: {self.name}'
    
    
#Property Region
class Region(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.name}-Region'

# Property City  
class City(models.Model):
    region = models.ForeignKey(Region,on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return f'Region-{self.region.name}--City-{self.name}'
    
#Property
class Property(models.Model):
    
    class PROPERTY_TYPE(models.TextChoices):
        Home = 'home', 'Home'
        APARTMENT = 'apartment','Apartment'
        HOSTEL = 'hostel','Hostel Room'
        
        
    class RENT_TYPE(models.TextChoices):
        MONTH = 'Month', 'Rent per Month'
        YEAR = 'YEAR', 'Rent per Year'
        
    class PROPERTY_STATUS(models.TextChoices):
        AVAILABLE = 'available','Available'
        BOOKED = 'booked', 'Booked'
        RENTED = 'rented', 'Rented'
    
    name = models.CharField(max_length=30)
    
    type = models.CharField(max_length=20,choices=PROPERTY_TYPE.choices) 
    
    beds = models.PositiveIntegerField()
    bath = models.PositiveIntegerField()
    wi_fi = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    
    main_photo = models.ImageField(upload_to='properties')
    bed_photo= models.ImageField(upload_to='properties',blank=True)
    bath_photo = models.ImageField(upload_to='properties',blank=True)
    pool_photo = models.ImageField(upload_to='properties',blank=True)
    
    rent_type = models.CharField(max_length=20,choices=RENT_TYPE.choices)
    rent_amount = models.PositiveIntegerField(default=0)
    
    region = models.ForeignKey(Region,on_delete=models.SET_NULL,null=True)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True)
    address = models.TextField(blank=True)
    
    posted_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='properties')
    created_at = models.DateField(auto_now=True)
    is_active = models.BooleanField()
    
    status = models.CharField(max_length=20,choices=PROPERTY_STATUS.choices)
    
    description = models.TextField()
    review_star = models.CharField(max_length=3)
    review_comment = models.TextField()
    
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f'{self.name}-{self.region}-{self.city}-{self.posted_by}'
