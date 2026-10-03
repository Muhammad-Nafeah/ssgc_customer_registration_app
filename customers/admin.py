from django.contrib import admin
from .models import CustomerRegistration


@admin.register(CustomerRegistration)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('UR_CONSUMER_S_NO', 'CLAIM_ID', 'FULL_NAME', 'CNIC', 'CITY', 'CASE_STATUS')
    search_fields = ('FULL_NAME', 'CNIC', 'CLAIM_ID')
    list_filter = ('REGION', 'CASE_STATUS')