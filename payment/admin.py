from django.contrib import admin

from .models import Payment


admin.site.site_title='Payment'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['paystack_reference', 'amount', 'payment_type','status', 'timestamp','user']
    list_display_links=["paystack_reference"]
    
