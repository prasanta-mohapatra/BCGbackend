from django.db import models

# Create your models here.


class Customer(models.Model):
    """ Customer Model having Fields are id, gender, income, region, marital_status, status and created_on """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    income = models.CharField(max_length=20)
    region = models.CharField(max_length=10)
    marital_status = models.BooleanField()
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Policy(models.Model):
    """ Policy Model having Fields are policy_id, date_of_purchase, customer_id, fuel_type, vehicle_segment, premium, body_injury_liability, personal_injury_liability, property_injury_liability, collision_liability, comprehensive_liability"""
    policy_id = models.BigIntegerField(primary_key=True)
    date_of_purchase = models.DateField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=10)
    vehicle_segment = models.CharField(max_length=5)
    premium = models.FloatField()
    body_injury_liability = models.BooleanField()
    personal_injury_liability = models.BooleanField()
    property_injury_liability = models.BooleanField()
    collision_liability = models.BooleanField()
    comprehensive_liability = models.BooleanField()

    def __str__(self):
        return self.policy_id
