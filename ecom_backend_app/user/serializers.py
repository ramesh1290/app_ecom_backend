from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate,get_user_model
 
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name',required=True)
    lastName = serializers.CharField(source='last_name',required=True)
    confirmPassword = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "firstName",
            "lastName",
            "email",
            "password",
            "confirmPassword",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmPassword"]:
            raise serializers.ValidationError(
                {"confirmPassword": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirmPassword")

        email = validated_data["email"]
        username = email

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user
    





class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "general": "Invalid email or password."
            })

        user = authenticate(username=user_obj.username, password=password)

        if not user:
            raise serializers.ValidationError({
                "general": "Invalid email or password."
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "general": "This account is inactive."
            })

        attrs["user"] = user
        return attrs