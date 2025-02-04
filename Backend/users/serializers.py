from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(style={'input_type':'password'},write_only=True, required=True)
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password"]

    def validate(self, data):
        
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"Passwords don't match."})
        
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password":list(e.messages)})

        return data

    def create(self, validated_data):
        
        validated_data.pop("confirm_password")  
        user = User.objects.create_user(**validated_data)
        return user
    


class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        data["user"] = user
        return data