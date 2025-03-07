# models.py
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

class Member(models.Model):
    PROFILE_CHOICES = [
        ("Myself", "Myself"), ("My Sister", "My Sister"), ("My Brother", "My Brother"),
        ("My Son", "My Son"), ("My Daughter", "My Daughter"), ("My Relative", "My Relative"),
        ("My Friend", "My Friend"),
    ]
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female")]
    RELIGION_CHOICES = [("Hindu", "Hindu"), ("Christian", "Christian"), ("Muslim", "Muslim")]
    MARITAL_STATUS_CHOICES = [
        ("Never Married", "Never Married"), ("Divorced", "Divorced"), 
        ("Annulled", "Annulled"), ("Widowed", "Widowed"), ("Nikah Divorce", "Nikah Divorce"), 
        ("Awaiting Divorce", "Awaiting Divorce"), ("Separated", "Separated"),
    ]
    BODY_TYPE_CHOICES = [
        ("Slim", "Slim"), ("Fit", "Fit"), ("Toned", "Toned"), ("Short", "Short"),
        ("Average", "Average"), ("Tall", "Tall"), ("Plus Size", "Plus Size"),
        ("Big and Tall", "Big and Tall"), ("Chubby", "Chubby"),
    ]
    EDUCATION_CHOICES = [
        ("Doctorate", "Doctorate"), ("Masters", "Masters"), ("Bachelors", "Bachelors"),
        ("Diploma", "Diploma"), ("High/Secondary School", "High/Secondary School"),
        ("Less than High School", "Less than High School"),
    ]
    COURSE_CHOICES = [
        ("MCA", "MCA"), ("MBA", "MBA"), ("MCom", "MCom"), ("MArch", "MArch"),
        ("Audiology", "Audiology"), ("IPS", "IPS"), ("IAS", "IAS"), ("IRS", "IRS"),
        ("MSc Nursing", "MSc Nursing"), ("MSc Agriculture", "MSc Agriculture"),
        ("MPharm", "MPharm"),
    ]
    DISTRICT_CHOICES = [
        ("Thrissur", "Thrissur"), ("Ernakulam", "Ernakulam"), ("Kottayam", "Kottayam"),
        ("Kannur", "Kannur"), ("Kasargod", "Kasargod"), ("Thiruvananthapuram", "Thiruvananthapuram"),
        ("Idukki", "Idukki"), ("Wayanad", "Wayanad"), ("Pathanamthitta", "Pathanamthitta"),
        ("Palakkad", "Palakkad"), ("Malappuram", "Malappuram"), ("Kollam", "Kollam"),
        ("Alappuzha", "Alappuzha"), ("Kozhikode", "Kozhikode"),
    ]
    CITY_CHOICES = [
        ("Neyyattinkara", "Neyyattinkara"), ("Varkala", "Varkala"), ("Aluva", "Aluva"),
        ("Angamaly", "Angamaly"), ("Perumbavoor", "Perumbavoor"), ("Feroke", "Feroke"),
        ("Kunnamangalam", "Kunnamangalam"), ("Guruvayur", "Guruvayur"),
        ("Chalakudy", "Chalakudy"), ("Karunagappally", "Karunagappally"),
        ("Punalur", "Punalur"), ("Changanassery", "Changanassery"),
        ("Pala", "Pala"), ("Manjeri", "Manjeri"), ("Tirur", "Tirur"),
    ]
    COMMUNITY_CHOICES = [
        ("Nair", "Nair"), ("Ezhava", "Ezhava"), ("Brahmin", "Brahmin"),
        ("Vishwakarma", "Vishwakarma"), ("Scheduled Caste (SC)", "Scheduled Caste (SC)"),
        ("Mappila", "Mappila"), ("Thangal", "Thangal"), ("Syrian Christian", "Syrian Christian"),
        ("Latin Catholic", "Latin Catholic"), ("Jacobite", "Jacobite"),
        ("Marthoma", "Marthoma"), ("Anglo-Indian", "Anglo-Indian"),
        ("Jewish", "Jewish"), ("Tribal", "Tribal"),
    ]
    FINANCIAL_STATUS_CHOICES = [
        ("Wealthy", "Wealthy"), ("Upper Middle Class", "Upper Middle Class"),
        ("Lower Middle Class", "Lower Middle Class"), ("Financially Stable", "Financially Stable"),
        ("Inherited Wealth", "Inherited Wealth"), ("Business Family", "Business Family"),
        ("Retired Family Income", "Retired Family Income"), ("Prefer Not to Say", "Prefer Not to Say"),
        ("Well-off", "Well-off"), ("Working Class", "Working Class"),
        ("Affluent", "Affluent"), ("Struggling Financially", "Struggling Financially"),
    ]
    
    FATHER_OCCUPATION_CHOICES = [
        ("Business", "Business"),
        ("IT", "IT"),
        ("Engineer", "Engineer"),
        ("Doctor", "Doctor"),
        ("Government Job", "Government Job"),
        ("Abroad", "Abroad"),
        ("Other", "Other"),
    ]
    
    MOTHER_OCCUPATION_CHOICES = [
        ("Business", "Business"),
        ("IT", "IT"),
        ("Engineer", "Engineer"),
        ("Doctor", "Doctor"),
        ("Government Job", "Government Job"),
        ("Home Maker", "Home Maker"),
        ("Other", "Other"),
    ]
    
    SIBLING_CHOICES = [
        ("Single Child", "Single Child"),
        ("Yes", "Yes"),
    ]
    
    SIBLING_OCCUPATION_CHOICES = [
        ("Studies", "Studies"),
        ("Engineer", "Engineer"),
        ("Doctor", "Doctor"),
        ("Government Job", "Government Job"),
        ("IT", "IT"),
        ("Other", "Other"),
    ]


    profile_for = models.CharField(max_length=20, choices=PROFILE_CHOICES)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254, blank=False, null=False,default="Not Specified", unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    age = models.IntegerField(null=True, blank=True)
    def clean(self):  # Validation method
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        if age < 21:
            raise ValidationError("You must be at least 21 years old to register.")
        
    def calculate_age(self):
        """Helper function to calculate age"""
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

    def save(self, *args, **kwargs):
        self.full_clean()  # Runs validation before saving
        self.age = self.calculate_age()  # Store calculated age
        super().save(*args, **kwargs)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    nationality = models.CharField(max_length=20, default="Indian")
    password = models.CharField(max_length=128)  # Storing hashed password
    height = models.IntegerField(choices=[(i, i) for i in range(100, 211)])
    weight = models.IntegerField(choices=[(i, i) for i in range(40, 111)])
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    physically_challenged = models.BooleanField(default=False)
    highest_education = models.CharField(max_length=30, choices=EDUCATION_CHOICES,null=False, blank=False, default="Not Specified")
    course = models.CharField(max_length=30, choices=COURSE_CHOICES)
    country = models.CharField(max_length=20, default="India")
    state = models.CharField(max_length=20, default="Kerala")
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    community = models.CharField(max_length=30, choices=COMMUNITY_CHOICES)
    financial_status = models.CharField(max_length=30, choices=FINANCIAL_STATUS_CHOICES)
    description = models.TextField()
    photo = models.ImageField(upload_to="profile_photos/",null=True,blank=True)
    
    #Family details
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_occupation = models.CharField(max_length=50, choices=FATHER_OCCUPATION_CHOICES, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=50, choices=MOTHER_OCCUPATION_CHOICES, blank=True, null=True)
    siblings = models.CharField(max_length=20, choices=SIBLING_CHOICES, default="Single Child")
    
    # Additional fields for siblings (visible only if siblings == "Yes")
    sibling_name = models.CharField(max_length=100, blank=True, null=True)
    sibling_occupation = models.CharField(max_length=50, choices=SIBLING_OCCUPATION_CHOICES, blank=True, null=True)

    # Job Details
    current_job = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    job_location = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Preferences(models.Model):
    user = models.OneToOneField('Member', on_delete=models.CASCADE)  # Link to Member model
    district = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(max_length=100, blank=True, null=True)
    community = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    financial_status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"
   
