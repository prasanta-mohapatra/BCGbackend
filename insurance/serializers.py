from rest_framework import serializers
from insurance.models import Customer, Policy


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'gender', 'income', 'region',
                  'marital_status', 'status', 'created_on')


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('policy_id', 'date_of_purchase', 'customer_id', 'fuel_type', 'vehicle_segment', 'premium', 'body_injury_liability',
                  'personal_injury_liability', 'property_injury_liability', 'collision_liability', 'comprehensive_liability')
