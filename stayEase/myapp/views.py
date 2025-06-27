from django.shortcuts import render,redirect
from django.views import View
from myapp.models import Property,AgencyProfile,Region,City
from django.shortcuts import get_object_or_404
from myapp.form import PropertyForm,RegionForm,CityForm,UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages 




def base(request):
    return render(request,'base.html')

def index(request):
    messages.info(request,f'Welcome {request.user.username}')
    return render(request,'index.html')


class PropertyView(View):
    def get(self,request):
        properties = Property.objects.all()
        context = {'properties':properties}
        return render(request,'property.html',context)
    
def propertyDetail(request,pk):
    property_detail = get_object_or_404(Property,id=pk)
    context = {'property':property_detail}
    return render(request, 'property-detail.html',context)

def propetyCreate(request):
    form = PropertyForm()
    context = {'form':form}
    if request.method == 'POST':
        form = PropertyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print("Successfully Created a New Property")
        else:
            print('Error Occur in Creating New Property')
            
        return render(request,'property-form.html',context)
    
    else:
        return render(request,'property-form.html',context)
    
    
    
def region(request):
    region_form = RegionForm()
    city_form = CityForm()
    
    cities = City.objects.all()
    regions = Region.objects.all()
    
    context = {'region_form':region_form,'regions':regions,'city_form':city_form,'cities':cities}
    
    if request.method == 'POST':
        if 'add_region' in request.POST:
            region_form = RegionForm(request.POST)
            if region_form.is_valid():
                region_form.save()
                print("New Region Created Successfully")
            else:
                print("Error Occur in Creating New Region")
            
        
        if 'add_city' in request.POST:
            city_form = CityForm(request.POST)
            if city_form.is_valid():
                city_form.save()
                print("Successfully Created new City")
            
            else:
                print("Error occur creating a new City")
                
        context = {
                'region_form':region_form,
                'regions':regions,
                'city_form':city_form,
                'cities':cities}  
                  
        return render(request,'region.html',context)
       
    
    else:
        
        return render(request, 'region.html',context)
    

#Delete Region
def delete_region(request,pk):
    region = get_object_or_404(Region,id=pk)
    region.delete()
    print('Successfully Deleted Region')

    return redirect('region')

#Delete City
def delete_city(request,pk):
    city = get_object_or_404(City,id=pk)
    city.delete()
    print("Successfully Deleted City")
    
    return redirect('region')

#Authentication
#Login
def login_user(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            
            authentication = authenticate(username=username,password=password)
            if authentication:
                login(request,authentication)
                print("login Successfully")
            else:
                print("Login Fail")
    
        return redirect('index')
    
    else:
        messages.info(request,'Hello Please login')
        return render(request,'login.html')
    
#Log Out
def logout_user(request):
    logout(request)
    print("Successfully Logout")
    return redirect('index')


#User Register
def register_user(request):
    register_form = UserCreationForm()
    register_user = True
    context = {'register_form':register_form,'register_user':register_user}
    
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
           new_user =  register_form.save()
           login(request,new_user)
           print("Registration Successful")
        else:
            print("Error Occur in Registration")
        
        return redirect('index')
        
    else:
        
        return render(request,'register.html',context)
    
    
    

