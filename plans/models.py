from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Plan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))])
    interval = models.CharField(max_length=10,choices=[('month','Month'),('3months','3 Months'),('year','Year')])
    stripe_product_id = models.CharField(max_length=100,blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired')
    ]
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='subscriptions')
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE,related_name='subscribers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)  
    auto_renew = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()