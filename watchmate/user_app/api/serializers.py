from django.contrib.auth.models import User
from rest_framework import serializers, exceptions


class RegistrationSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmPassword"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        password = self.validated_data["password"]
        confirmPassword = self.validated_data["confirmPassword"]

        if password != confirmPassword:
            raise exceptions.ValidationError("Sorry, passwords do not match")
