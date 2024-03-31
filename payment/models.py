from django.db import models
from core.models import User 


# Create your models here.
class TimestampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']




class Payment(models.Model):
    PAYMENT_TYPE = (
        ("DC", "Debit Card"),
        ("BT", "Bank Transfer")
    )
    paystack_reference=models.CharField(max_length=200, unique=True)
    amount=models.CharField(max_length=80)
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPE, default="DC")
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="payment")
    
