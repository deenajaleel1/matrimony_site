from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "phone", "gender", "dob", "marital_status")
    search_fields = ("name", "username", "phone")




