from __future__ import division

import datetime

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from api.models import *

class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        update_last_login(None, validated_data["user"])
        return validated_data

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "account_type", "password")


class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        rep.pop("password", None)
        return rep

    class Meta:
        model = User
        fields = "__all__"
        write_only_fields = ("password",)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=120)
    new_password = serializers.CharField(max_length=120)

# BATTALLION FIVE SERIALIZER 
class BattallionSixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battallion_six
        fields = "__all__"

# BATTALLION FIVE SERIALIZER 
class BattallionFiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battallion_five
        fields = "__all__"

# BATTALLION FOUR SERIALIZER 
class BattallionFourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battallion_four
        fields = "__all__"

# BATTALLION THREE SERIALIZER 
class BattallionThreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battallion_three
        fields = "__all__"

# BATTALLION TWO SERIALIZER 
class BattallionTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battallion_two
        fields = "__all__"

# BATTALLION ONE SERIALIZER 
class BattallionOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battallion_one
        fields = "__all__"

class DeletedEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deleted_Employee
        fields = "__all__"

