from django.contrib import admin
from .models import Member, Contact

class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "expiry_date")
    list_filter = ("expiry_date",)
    search_fields = ("name",)
    ordering = ("join_date",)
    readonly_fields = ("join_date",)  
    
admin.site.register(Member, MemberAdmin)
admin.site.register(Contact)
