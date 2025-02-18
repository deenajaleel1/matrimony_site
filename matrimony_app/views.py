from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from matrimony_app.models import Member
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from datetime import date

# Create your views here.
# matrimony_app/views.py

def matrimony_home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            # Fetch the user from the custom Member model
            user = Member.objects.get(username=username)
            
            # Check if the provided password matches the stored hashed password
            if check_password(password, user.password):
                request.session["user_id"] = user.id  # Store user session
                request.session["username"] = user.username  # Store username
                messages.success(request, "Login successful!")
                return redirect("profile")  # Redirect to profile page
            else:
                messages.error(request, "Invalid username or password")
        except Member.DoesNotExist:
            messages.error(request, "Invalid username or password")
        
        return redirect("login")  # Redirect back to login page if authentication fails
    return render(request, 'login.html')

def registration_view(request):
    if request.method=="POST":
        profile_for=request.POST.get('profile_for')
        name=request.POST.get('name')
        username=request.POST.get('username')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        religion=request.POST.get('religion')
        nationality=request.POST.get('nationality')
        password=request.POST.get('password')
        height=request.POST.get('height')
        weight=request.POST.get('weight')
        marital_status=request.POST.get('marital_status')
        body_type=request.POST.get('body_type')
        physically_challenged=request.POST.get('physically_challenged')
        highest_education=request.POST.get('highest_education')
        course=request.POST.get('course')
        country=request.POST.get('country')
        state=request.POST.get('state')
        district=request.POST.get('district')
        city=request.POST.get('city')
        community=request.POST.get('community')
        financial_status=request.POST.get('financial_status')
        description=request.POST.get('description')
        photo=request.FILES.get('photo')
        
        # Debugging: Check if photo is received
        if photo:
            print("Photo received:", photo.name)
        else:
            print("No photo received")
        
         # ✅ Convert dob to date object
        dob = date.fromisoformat(dob)  # dob should be in YYYY-MM-DD format
        
        # ✅ Calculate age
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        # ✅ Check if user is 21 or older
        if age < 21:
            messages.error(request, "You must be at least 21 years old to register.")
            return redirect("registration")  # Redirect to registration page if underage
        
        # ✅ Password Strength Validation
        try:
            validate_password(password)  # Check password strength
        except ValidationError as e:
            messages.error(request, e.messages[0])  # Show validation error
            return redirect("registration")  # Redirect to registration page
        
        # ✅ Hash the Password Before Saving
        hashed_password = make_password(password)
        
        register=Member(profile_for=profile_for,name=name,username=username,phone=phone,email=email,gender=gender,dob=dob,religion=religion,nationality=nationality,password=hashed_password,height=height,weight=weight,marital_status=marital_status,body_type=body_type,physically_challenged=physically_challenged,highest_education=highest_education,course=course,country=country,state=state,district=district,city=city,community=community,financial_status=financial_status,description=description,photo=photo)
        register.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')
    return render(request, 'registration.html')

def profile_view(request):
    user_id = request.session.get("user_id")  # Get user ID from session
    if not user_id:
        messages.error(request, "You need to log in first.")
        return redirect("login")  # Redirect to login if no user is in session

    try:
        member = Member.objects.get(id=user_id)  # Fetch the logged in member 
        opposite_gender = "Female" if member.gender == "Male" else "Male"
        opposite_profiles = Member.objects.filter(gender=opposite_gender)  # Fetch opposite gender profiles
        print("Found opposite gender profiles:", opposite_profiles.count())  # Debugging line
        return render(request, 'profile.html', {"member": member, "opposite_profiles": opposite_profiles})
    except Member.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("login")
    #return render(request, 'profile.html')

def edit_profile(request):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "You need to log in first.")
        return redirect("login")

    try:
        member = Member.objects.get(id=user_id)
        if request.method == "POST":
            # Process form submission here (update member details)
            member.name = request.POST.get("name", member.name)
            member.dob = request.POST.get("dob", member.dob)
            member.country = request.POST.get("country", member.country)
            # Add other fields here...
            member.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

        return render(request, "edit_profile.html", {"member": member})
    except Member.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("login")

def edit_preferences(request):
    return redirect('login')

def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

