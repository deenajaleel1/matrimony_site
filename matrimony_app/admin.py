from django.contrib import admin
from .models import Member, Chat


    
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "phone", "gender", "dob", "marital_status")
    search_fields = ("name", "username", "phone")
   

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message_preview', 'timestamp')
    search_fields = ('sender__name', 'receiver__name', 'message')
    list_filter = ('timestamp',)

    def message_preview(self, obj):
        return obj.message[:50]  # Show first 50 characters in admin panel

    message_preview.short_description = "Message"
