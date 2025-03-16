from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from matrimony_app.models import Member, Chat 
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from datetime import date,timedelta
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q,Max
from django.db.models import F
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse

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
        # Family Details
        father_name = request.POST.get("father_name", "")
        father_occupation = request.POST.get("father_occupation", "")
        mother_name = request.POST.get("mother_name", "")
        mother_occupation = request.POST.get("mother_occupation", "")
        siblings = request.POST.get("siblings", "Single Child")  # Default is Single Child
        
        # Sibling details (only if "Yes" is selected)
        sibling_name = request.POST.get("sibling_name", "") if siblings == "Yes" else None
        sibling_occupation = request.POST.get("sibling_occupation", "") if siblings == "Yes" else None
        
        # Job Details
        current_job = request.POST.get("current_job", "")
        company_name = request.POST.get("company_name", "")
        job_location = request.POST.get("job_location", "")

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
        
        register=Member(profile_for=profile_for,name=name,username=username,phone=phone,email=email,gender=gender,dob=dob,religion=religion,nationality=nationality,password=hashed_password,height=height,weight=weight,marital_status=marital_status,body_type=body_type,physically_challenged=physically_challenged,highest_education=highest_education,course=course,country=country,state=state,district=district,city=city,father_name=father_name,
            father_occupation=father_occupation,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            siblings=siblings,
            sibling_name=sibling_name,
            sibling_occupation=sibling_occupation,current_job=current_job,
            company_name=company_name,
            job_location=job_location,community=community,financial_status=financial_status,description=description,photo=photo)
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
    
    
def profile_detail(request, id):
    profile_user = get_object_or_404(Member, id=id)  # Fetch user by id
    return render(request, 'profile_detail.html', {'user': profile_user})  # Send data to template


def matches(request):
    return render(request,'matches.html')


def search_matches(request):
    user_id = request.session.get("user_id")  # Get user ID from session
    if not user_id:
        messages.error(request, "You need to log in first.")
        return redirect("login")
        
    logged_in_member = Member.objects.get(id=user_id)
    
    matches=[]

    if request.method == "POST":
        district = request.POST.get("district", "").strip()
        religion = request.POST.get("religion", "").strip()
        community = request.POST.get("community", "").strip()
        marital_status = request.POST.get("marital_status", "").strip()
        financial_status = request.POST.get("financial_status", "").strip()

        # Determine opposite gender
        opposite_gender = "Female" if logged_in_member.gender == "Male" else "Male"

        # Filter members based on search criteria
        matches = Member.objects.filter(
            gender=opposite_gender
        )
        
        if district:
            matches = matches.filter(district__iexact=district)
        if religion:
            matches = matches.filter(religion__iexact=religion)
        if community:
            matches = matches.filter(community__iexact=community)
        if marital_status:
            matches = matches.filter(marital_status__iexact=marital_status)
        if financial_status:
            matches = matches.filter(financial_status__iexact=financial_status)
            
        matches=matches.exclude(id=logged_in_member.id)  # Exclude the logged-in user
        print(matches)
        return render(request, "match_results.html", {"matches": matches})
    return redirect("matches")  # Redirect to matches page if no search was performed

def chat_view(request, receiver_id):
    sender_id = request.session.get('user_id')  # Get logged-in user's ID from session
    sender = get_object_or_404(Member, id=sender_id)
    receiver = get_object_or_404(Member, id=receiver_id)  # Fetch the receiver
    
    # Fetch messages between sender and receiver
    messages = Chat.objects.filter(
        sender__in=[sender, receiver], receiver__in=[sender, receiver]
    ).order_by('timestamp')
    
    return render(request, 'chat.html', {"receiver": receiver,'messages': messages})

def send_message(request, receiver_id):
    print("Request method:", request.method)  # Debugging line
    print("Session data:", request.session.items())  # Print entire session
    if request.method == "POST":
        sender_id = request.session.get('user_id')  # Get logged-in user ID
        print("Sender ID from session:", sender_id)  # Debugging sender_id
        sender = get_object_or_404(Member, id=sender_id)
        receiver = get_object_or_404(Member, id=receiver_id)

        message = request.POST.get('message', '').strip()  # Extract message text
        if message:
            Chat.objects.create(sender=sender, receiver=receiver, message=message)
            return HttpResponse("success")  # Simple text response
        else:
            return HttpResponse("Message cannot be empty.", status=400)

    return HttpResponse("Invalid request method.", status=405)

def recent_chats(request):
    user_id = request.session.get('user_id')  # Get logged-in user's ID
    user = get_object_or_404(Member, id=user_id)

    # Get all distinct users the logged-in user has interacted with
    recent_chat_users = Member.objects.filter(
        Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
    ).distinct().annotate(last_message_time=Max('sent_messages__timestamp'))

    # Sort users by last message time (descending order)
    recent_chat_users = recent_chat_users.order_by('-last_message_time')

    # Fetch the last message exchanged with each user
    recent_chats = []
    for chat_user in recent_chat_users:
        last_message = Chat.objects.filter(
            (Q(sender=user, receiver=chat_user) | Q(sender=chat_user, receiver=user))
        ).order_by('-timestamp').first()

        if last_message:
            recent_chats.append({
                'user': chat_user,
                'last_message': last_message.message,
                'timestamp': last_message.timestamp
            })

    return render(request, 'recent_chats.html', {'recent_chats': recent_chats})


def search_users(request):
    query = request.GET.get('q', '')  # Get the search query from the input box
    print("Search Query:", query)  # Debugging - Check if query is received
    users = Member.objects.filter(name__icontains=query) if query else []  # Filter users by name (case-insensitive)
    print("Matching Users:", users)  # Debugging - Check if users are found in the database
    return render(request, 'search.html', {'users': users, 'query': query})  # Pass data to the template


def edit_profile(request):
    return redirect('edit_profile')


def edit_preferences(request):
    return redirect('login')

def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

