from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

#from django.contrib.auth.models import User


class TripSerializer(serializers.ModelSerializer):
	class Meta:
		model = Trips
		fields ='__all__'

class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendors
		fields ='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ['mobile']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = "__all__"
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = "__all__"
