from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Property, AgencyProfile, OwnerProfile, Region, City, CustomUser,SaveProperty,Inquiry
from myapp.form import CustomerProfileForm, AgencyProfileForm, OwnerProfileForm, RegionForm, CityForm, PropertyForm,ReviewForm,UserRegistrationForm,InquiryForm
from django.db.models import Avg

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.contrib.auth.models import User

# dashboard/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Avg
from django.db.models.functions import Lower
from myapp.models import Property, CustomUser, Review

def base(request):
    return render(request, 'base.html')
   

def index(request):
    # Check user type using a more reliable approach
    if hasattr(request.user, 'role') and request.user.role == 'CUSTOMER':
      
        messages.info(request, f'Welcome {request.user.username}')
        
        # Common context for both GET and POST
        regions = Region.objects.all()
        cities = City.objects.all()
        
        if request.method == 'POST':
            # Get filter parameters with default None values
            region_id = request.POST.get('region')
            township_id = request.POST.get('township')
            property_type_value = request.POST.get('property_type')

            # Start with all properties
            search_properties = Property.objects.all()
            region_obj = None
            township_obj = None

            # Apply filters sequentially
            if region_id:
                region_obj = Region.objects.filter(id=region_id).first()
                if region_obj:
                    search_properties = search_properties.filter(region=region_obj)

            if township_id:
                township_obj = City.objects.filter(id=township_id).first()
                if township_obj:
                    search_properties = search_properties.filter(city=township_obj)

            if property_type_value:
                search_properties = search_properties.filter(property_type=property_type_value)
            
            saved_porperties = SaveProperty.objects.filter(user = request.user)
            save_property = SaveProperty.objects.filter(user=request.user.id)
            save_property_list = SaveProperty.objects.filter(user=request.user).values_list('property_id', flat=True)
            featured_properties = Property.objects.filter(is_featured=True,admin_approved ='APPROVED' )
            yangon_properties = Property.objects.filter(region = 1)
            mandalay_properties = Property.objects.filter(region = 2)    

            context = {
                'search_properties': search_properties,
                'region': region_obj,
                'township': township_obj,
                'property_type': property_type_value,
                'regions': regions,  # Maintain form options
                'cities': cities,    # Maintain form options,
                
                'featured_properties': featured_properties,
                'regions': regions,
                'cities': cities,
                'saved_porperties':saved_porperties,
                'save_property':save_property,
                'save_property_list':save_property_list,
                'yangon_properties':yangon_properties,
                'mandalay_properties':mandalay_properties
            }
            return render(request, 'index.html', context)
        
        # Handle GET request
        saved_porperties = SaveProperty.objects.filter(user = request.user)
        save_property = SaveProperty.objects.filter(user=request.user.id)
        save_property_list = SaveProperty.objects.filter(user=request.user).values_list('property_id', flat=True)
        featured_properties = Property.objects.filter(is_featured=True,admin_approved ='APPROVED' )
        yangon_properties = Property.objects.filter(region = 1)
        mandalay_properties = Property.objects.filter(region = 2)
        context = {
            'featured_properties': featured_properties,
            'regions': regions,
            'cities': cities,
            'saved_porperties':saved_porperties,
            'save_property':save_property,
            'save_property_list':save_property_list,
            'yangon_properties':yangon_properties,
            'mandalay_properties':mandalay_properties
            
            
        }
        return render(request, 'index.html', context)
    
    # Handle other user types
    elif hasattr(request.user, 'role') and request.user.role == 'AGENCY':
        return redirect('agency_dashboard')
    
    elif hasattr(request.user, 'role') and request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    
    # Default case (admin or unknown)
    return redirect('login_user')  # Fixed typo in URL name

# class PropertyView(View):
#     def get(self, request):
#         propertyForm = PropertyForm()
#         active_properties = Property.objects.filter(is_active=True)
#         context = {'active_properties': active_properties, 'form': propertyForm}
#         return render(request, 'property.html', context=context)
    
#     def post(self, request):
#         propertyForm = PropertyForm(request.POST, request.FILES)
#         if propertyForm.is_valid():
#             property = propertyForm.save(commit=False)
#             property.posted_by = request.user  # ✅ Set the posted_by field
#             property.save()
#             print("Successfully Created New Property")
#         else:
#             print("Error Creating New Property")
#         return redirect('property')
    
# def adminDashboard(request):
#     if request.user.is_authenticated:
#         return render(request,'admin-dashboard.html')






@staff_member_required
def admin_dashboard(request):
    # Stats data
    total_users = CustomUser.objects.count()
    print(total_users-1)
    properties_listed = Property.objects.count()
    agencies_registered = CustomUser.objects.filter(role='AGENCY').count()  # Fixed role filter
    average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    pending_properties = Property.objects.filter( admin_approved = 'PENDING')
    recent_logs = LogEntry.objects.select_related('content_type')\
    .order_by('-action_time')[:10]  # limit to last 10 actions
    
    # Property type distribution - case-insensitive grouping
    property_types = (
        Property.objects
        .annotate(lower_type=Lower('property_type'))
        .values('lower_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    property_labels = [p['lower_type'].capitalize() for p in property_types]
    property_counts = [p['count'] for p in property_types]
    
    # User distribution
    user_types = [
        {'type': 'Customers', 'count': CustomUser.objects.filter(role='CUSTOMER').count()},
        {'type': 'Owners', 'count': CustomUser.objects.filter(role='OWNER').count()},
        {'type': 'Agencies', 'count': agencies_registered},
        {'type': 'Admins', 'count': CustomUser.objects.filter(is_staff=True).count()},
    ]
    
    context = {
        'total_users': total_users-agencies_registered-1,
        'properties_listed': properties_listed,
        'agencies_registered': agencies_registered,
        'average_rating': round(average_rating, 1),
        'property_labels': property_labels,
        'property_counts': property_counts,
        'user_types': user_types,
        'pending_properties':pending_properties,
        'recent_logs':recent_logs
    }
    
    print(f'pendign properties {pending_properties}')
    
    return render(request, 'admin-dashboard.html', context)









class PropertyView(View):
    def get(self, request):
        propertyForm = PropertyForm()
        cities = City.objects.all()
        properties = Property.objects.filter(is_active=True ,admin_approved = 'APPROVED')
        saved_porperties = SaveProperty.objects.filter(user = request.user)
        save_property = SaveProperty.objects.filter(user=request.user.id)
        save_property_list = SaveProperty.objects.filter(user=request.user).values_list('property_id', flat=True)


        # Filtering logic
        city = request.GET.get('city')
        property_type = request.GET.get('property_type')
        beds = request.GET.get('beds')

        if city:
            properties = properties.filter(city__name__icontains=city)

        if property_type:
            properties = properties.filter(property_type=property_type)

        if beds:
            if beds == '4':
                properties = properties.filter(beds__gte=4)
            else:
                properties = properties.filter(beds=beds)

        context = {
            'active_properties': properties,
            'form': propertyForm,
            'cities': cities,
            'saved_porperties':saved_porperties,
            'save_property_list':save_property_list,
            'save_property':save_property
        }
        
        print(saved_porperties)
        return render(request, 'property.html', context)

    def post(self, request):
        propertyForm = PropertyForm(request.POST, request.FILES)
        if propertyForm.is_valid():
            property = propertyForm.save(commit=False)
            property.posted_by = request.user
            property.save()
        return redirect('property')


class PropertyDetailView(View):
    def get(self, request, pk):
        property_obj = get_object_or_404(Property, id=pk )
        inquiry_form = InquiryForm()
        review_form = ReviewForm()
        reviews = property_obj.reviews.filter(is_approved=True)
        average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

        context = {
            'property': property_obj,
            'review_form': review_form,
            'reviews': reviews,
            'inquiryForm': inquiry_form,
            'average_rating': average_rating
        }
        return render(request, 'property-detail.html', context)
    
    def post(self, request, pk):
        property = get_object_or_404(Property, id=pk)
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            # Check for duplicate review
            if Review.objects.filter(property=property, user=request.user).exists():
                messages.warning(request, "You have already submitted a review for this property.")
                return redirect('property_detail', pk=pk)
            review = form.save(commit=False)
            review.property = property
            review.user = request.user
            review.save()
            messages.success(request, "Review submitted for approval!")
        else:
            messages.error(request, "Something went wrong")
            print("error")
        return redirect('property_detail', pk=pk)

class AgencyView(View):
    def get(self, request):
        agency_user = CustomUser.objects.filter(role='AGENCY')
        print(agency_user)
        agencies = AgencyProfile.objects.filter(user__in=agency_user)
        context = {'agencies': agencies}
        return render(request, 'agency.html', context)

class AgencyDetailView(View):
    def get(self, request, pk):
        agency = get_object_or_404(CustomUser, id=pk)
        posted_properties = Property.objects.filter(posted_by=agency)
        agencyProfileForm = AgencyProfileForm()
        agencyProfile = AgencyProfile.objects.filter(user=agency)
        context = {'agency': agency, 'posted_properties':posted_properties,'agencyProfileForm':agencyProfileForm,'agencyProfile':agencyProfile}
        
        #test
        print(agency,posted_properties)
        
        return render(request, 'agency-detail.html', context)
    
    def post(self,request,pk):
        agency = get_object_or_404(CustomUser, id=pk)
        posted_properties = Property.objects.filter(posted_by=agency)
        agencyProfileForm = AgencyProfileForm(request.POST,request.FILES)
        context = {'agency': agency, 'posted_properties':posted_properties,'agencyProfileForm':agencyProfileForm}

        # Check if profile already exists
        if AgencyProfile.objects.filter(user=agency).exists():
            messages.error(request, "This agency already has a profile.")
            return render(request, 'agency-detail.html', context)

        if agencyProfileForm.is_valid():
            agency_profile = agencyProfileForm.save(commit=False)
            agency_profile.user = agency
            agency_profile.save()
            messages.success(request, "Successfully Created Agency Profile")
        else:
            messages.error(request, "Error Creating Agency Profile")

        return render(request, 'agency-detail.html', context)
        
        

class OwnerView(View):
    def get(self, request):
        owners = OwnerProfile.objects.all()
        context = {'owners': owners}
        return render(request, 'owner.html', context)

class OwnerDetailview(View):
    def get(self, request, pk):
        owner = get_object_or_404(OwnerProfile, id=pk)
        context = {'owner': owner}
        return render(request, 'owner-detail.html', context)

class LocationView(View):
    def get(self, request):
        regionForm = RegionForm()
        cityForm = CityForm()
        regions = Region.objects.all()
        cities = City.objects.all()
        context = {'regions': regions, 'cities': cities, 'regionForm':regionForm,'cityForm':cityForm}
        return render(request, 'location.html', context)
    
    def post(self,request):
        regionForm = RegionForm(request.POST)
        if regionForm.is_valid():
            regionForm.save()
            print("Successfully Create New Region")

        else:
            print("Error creating New Region")
            
        cityForm = CityForm(request.POST)
        if cityForm.is_valid():
            cityForm.save()
            print("Successfully Create New City")
        else:
            print("Error Creating New City")
        
        return redirect('location')


# class ServiceView(View):
#     def get(self, request):
#         return render(request, 'service.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        authenticatedUser = authenticate(request,username=username, password=password)
        if authenticatedUser:
            login(request, authenticatedUser)
            print("Successful login")
            print(f'User Name:{username} , Password: {password}')
            
            messages.success(request, f'Welcome back, {authenticatedUser.username}!')
            
            if request.user.role == 'CUSTOMER':
            
                return redirect('index')
            
            elif request.user.role == 'AGENCY':
                return redirect('agency_dashboard')
            
            else : 
                return render (request,'admin-dashboard.html')
            
            
        else:
            print("Error Login")
            print(username,password)
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'loginUser.html')

def logout_user(request):
    logout(request)
    print("Successful Logout")
    messages.info(request, 'You have been logged out.')
    return redirect('index')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ✅ This will hash the password correctly
            login(request,user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registerUser.html', {'form': form})


    




class ProfileView(View):
    def get_profile_context(self, user):
        profile = None
        form = None
        profile_type = None
        return profile, form, profile_type

    def get(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to view your profile')
            return redirect('login')
        
        inquiry_list = Inquiry.objects.filter(agency_owner=request.user)
        customer_inquiry = Inquiry.objects.filter(customer = request.user)
    
        sp_list = SaveProperty.objects.filter(user=request.user)
        featured_properties = Property.objects.filter(is_featured=True,admin_approved ='APPROVED' )

        profile, form, profile_type = self.get_profile_context(request.user)

        saved_porperties = SaveProperty.objects.filter(user = request.user)
        save_property = SaveProperty.objects.filter(user=request.user.id)
        save_property_list = SaveProperty.objects.filter(user=request.user).values_list('property_id', flat=True)
       
        
        return render(request, 'profile.html', {
            'form': form,
            'profile': profile,
            'profile_type': profile_type,
            'user_role': request.user.get_role_display(),
            'sp_list':sp_list,
            'inquiry_list': inquiry_list,
            'customer_inquiry':customer_inquiry,
            'saved_porperties':saved_porperties,
            'save_property':save_property,
            'save_property_list':save_property_list
            
            
            
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        profile, _, profile_type = self.get_profile_context(request.user)

        if not profile:
            messages.error(request, "Profile update not available for your role")
            return redirect('profile')

        # Determine the correct form class
        form_class_map = {
            'customer': CustomerProfileForm,
            'agency': AgencyProfileForm,
            'owner': OwnerProfileForm
        }
        form_class = form_class_map.get(profile_type)

        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

        return render(request, 'profile.html', {
            'form': form,
            'profile': profile,
            'profile_type': profile_type,
            'user_role': request.user.get_role_display(),
        })
        

# class SavePropertyView(View):
#     def get(self,request,pk):
#         user_id = request.user.id
        
#         user_obj = get_object_or_404(CustomUser,id=user_id)
        
#         property_obj = get_object_or_404(Property,id=pk)
        
#         if not SaveProperty.objects.filter(user=user_obj,property=property_obj).exists():
#             SaveProperty.objects.create(user=user_obj,property=property_obj)
#             print(user_obj,property_obj,'Successfully Save')
#             messages.success(request, "Inquiry sent successfully!")
#         else:
#             print(user_obj,property_obj,"Already Exists")
#             messages.warning(request, "You have already sent an inquiry for this property.")
        
        
#         return redirect('property')
    
#     def post(self,request,pk):
#         pass



from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import SaveProperty, Property, CustomUser


class SavePropertyView(View):
    
    
    def post(self, request, pk):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please login to save properties'}, status=403)
            messages.error(request, "Please login to save properties")
            return redirect('login')
        
        user = request.user
        property_obj = get_object_or_404(Property, id=pk)
        
        saved_property, created = SaveProperty.objects.get_or_create(
            user=user,
            property=property_obj
        )
        
        if not created:
            saved_property.delete()
            action = 'unsaved'
            message = "Property removed from your saved list"
        else:
            action = 'saved'
            message = "Property added to your saved list"
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'action': action,
                'message': message,
                'saved_count': SaveProperty.objects.filter(property=property_obj).count()
            })
        
        messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER', 'property_detail', kwargs={'pk': pk}))
    


def sendInquiry(request, pk):
    if request.method == 'POST':
        customer = request.user
        property_obj = get_object_or_404(Property, id=pk)
        agency_owner = property_obj.posted_by
        message = request.POST['inquiryMessage']

        print(customer, property_obj, agency_owner, message)

        # Check for duplicate inquiry
        if Inquiry.objects.filter(customer=customer, property=property_obj).exists():
            messages.warning(request, "You have already sent an inquiry for this property.")
            print("You have already sent an inquiry for this property.")
            return redirect('property_detail', pk=pk)
        
        Inquiry.objects.create(
            customer=customer,
            agency_owner=agency_owner,
            property=property_obj,
            message=message
        )
        messages.success(request, "Inquiry sent successfully!")
        print('Inquiry sent successfully!')

    return redirect('property_detail', pk=pk)
    #return redirect('property')

def cancelInquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, id=pk)
    # Only allow the customer or agency_owner to cancel their own inquiry
    if request.user == inquiry.customer or request.user == inquiry.agency_owner:
        
        property_obj = inquiry.property 
        property_obj.status = 'AVAILABLE'
        property_obj.save()
        
        inquiry.delete()
        messages.success(request, "Inquiry cancelled successfully!")
        print("Inquiry cancelled successfully!")
    else:
        messages.error(request, "You do not have permission to cancel this inquiry.")
        print("You do not have permission to cancel this inquiry.")
    return redirect('profile')


@login_required
def approveInquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, id=pk)

    if request.user != inquiry.agency_owner:
        messages.error(request, "You are not authorized to approve this inquiry.")
        return redirect('inquiry_detail', pk)

    if not inquiry.is_approved:
        inquiry.is_approved = True
        inquiry.save()
        inquiry.property.status = 'BOOKED'  # Make sure this matches your STATUS_CHOICES
        inquiry.property.save()
        messages.success(request, "Inquiry approved and property status updated.")
    else:
        messages.info(request, "This inquiry has already been approved.")

    return redirect('inquiry_detail', pk)

@login_required
def rejectInquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, id=pk)

    if request.user != inquiry.agency_owner:
        messages.error(request, "You are not authorized to reject this inquiry.")
        return redirect('inquiry_detail', id=pk)

    # Mark as rejected or delete
    property_obj = inquiry.property 
    property_obj.status = 'AVAILABLE'
    property_obj.save()
    inquiry.delete()
    messages.success(request, "Inquiry rejected and deleted successfully.")
    print("Inquiry rejected and deleted successfully.")
    return redirect('profile')


def inquiryDetail(request, pk):
    inquiry = get_object_or_404(Inquiry, id=pk)
    context = {'inquiry':inquiry}
    return render(request, 'inquiry-detail.html',context)


@login_required
def payment(request, pk):  # `pk` is the Inquiry ID
    # Step 1: Get the Inquiry
    inquiry = get_object_or_404(Inquiry, id=pk)

    # Step 2: Check permission
    if request.user != inquiry.customer:
        messages.error(request, "You are not allowed to make this payment.")
        return redirect('profile')

    # Step 3: Perform payment logic (simulated here)
    # In real world, you'd integrate with Stripe, PayPal, etc.

    # Step 4: Change property status to 'RENTED'
    property_obj = inquiry.property
    property_obj.status = 'RENTED'
    property_obj.save()

    messages.success(request, f"Payment successful! Property '{property_obj.name}' is now rented.")
    print("Payment successful! Property status updated to RENTED.")
    
        
        
    return redirect('profile')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Property, Inquiry, Review
from myapp.form import PropertyForm  # Ensure this import exists

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Property, Inquiry, Review
from .form import PropertyForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Property, Inquiry, Review
from .form import PropertyForm

@login_required
def agencyDashboard(request):
    # Verify user role
    if request.user.role != 'AGENCY':
        return redirect('index')
    
    # Handle all POST requests (create, update, delete)
    if request.method == 'POST':
        # Property creation
        if 'create_property' in request.POST:
            propertyForm = PropertyForm(request.POST, request.FILES)
            if propertyForm.is_valid():
                property = propertyForm.save(commit=False)
                property.posted_by = request.user
                property.save()
                messages.success(request, f"Successfully created new property: {property.name}")
            else:
                messages.error(request, "Error occurred while creating new property.")
            return redirect('agency_dashboard')
        
        # Property update
        elif 'update_property' in request.POST:
            property_id = request.POST.get('property_id')
            property = get_object_or_404(Property, id=property_id, posted_by=request.user)
            propertyForm = PropertyForm(request.POST, request.FILES, instance=property)
            if propertyForm.is_valid():
                propertyForm.save()
                messages.success(request, f"Successfully updated property: {property.name}")
            else:
                messages.error(request, "Error occurred while updating property.")
            return redirect('agency_dashboard')
        
        # Property deletion
        elif 'delete_property' in request.POST:
            property_id = request.POST.get('property_id')
            property = get_object_or_404(Property, id=property_id, posted_by=request.user)
            property_name = property.name
            property.delete()
            messages.success(request, f"Successfully deleted property: {property_name}")
            return redirect('agency_dashboard')
    
    # Prepare dashboard data - CORRECTED INDENTATION
    properties = Property.objects.filter(posted_by=request.user).order_by('-created_at')
    
    # Attach edit form to each property instance
    for property in properties:
        property.edit_form = PropertyForm(instance=property)
    
    inquiries = Inquiry.objects.filter(agency_owner=request.user).order_by('-created_at')
    reviews = Review.objects.filter(property__posted_by=request.user).order_by('-created_at')
    
    # Prepare recent activities
    recent_activities = []
    
    # Add recent properties
    recent_activities.extend({
        'date': prop.created_at,
        'type': 'Property Added',
        'property': prop.name,
        'status': prop.get_status_display(),
        'status_color': 'success' if prop.status == 'AVAILABLE' else 'warning'
    } for prop in properties[:3])
    
    # Add recent inquiries
    recent_activities.extend({
        'date': inquiry.created_at,
        'type': 'New Inquiry',
        'property': inquiry.property.name,
        'status': 'Pending' if not inquiry.is_approved else 'Approved',
        'status_color': 'warning' if not inquiry.is_approved else 'success'
    } for inquiry in inquiries[:3])
    
    # Sort activities by date (newest first)
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    
    # Create form instance for new property
    propertyForm = PropertyForm()
    
    context = {
        'agency_profile': getattr(request.user, 'agency_profile', None),
        'properties': properties,
        'properties_count': properties.count(),
        'active_properties_count': properties.filter(status='AVAILABLE').count(),
        'inquiry_list': inquiries,
        'new_inquiries_count': inquiries.filter(is_approved=False).count(),
        'property_reviews': reviews,
        'pending_reviews_count': reviews.filter(is_approved=False).count(),
        'recent_activities': recent_activities[:5],
        'form': propertyForm
    }
    
    return render(request, 'agency-dashboard.html', context)        
    #     form = InquiryForm(request.POST)
    #     if form.is_valid():
    #         inquiry = form.save(commit=False)
    #         inquiry.customer = request.user
    #         inquiry.save()
    #         return redirect('inquiry_sent')  # You can customize this
    # else:
    #     form = InquiryForm()
    # return render(request, 'inquiry/send_inquiry.html', {'form': form})

# def approveInquiry(request,inquiry_id):
#     inquiry = get_object_or_404(Inquiry,id=inquiry_id)
    
#     if request.method == 'POST':
#         inquiry.approve()
#         return redirect('inquiry_list')



def service(request):
    return render(request,'base/service.html')

def about(request):
    return render(request,'base/about.html')

def contact(request):
    return render(request,'base/contact.html')


def agencySetting(request):
    return render(request,'agency-setting.html')






