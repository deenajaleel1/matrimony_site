from django.contrib import admin
from .models import Member, Preferences

class PreferencesInline(admin.StackedInline):  # Display Preferences inside Member
    model = Preferences
    can_delete = False  
    extra = 0  # Don't show extra empty fields
    
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "phone", "gender", "dob", "marital_status")
    search_fields = ("name", "username", "phone")
    inlines = [PreferencesInline]  # Attach Preferences inside Member profile


