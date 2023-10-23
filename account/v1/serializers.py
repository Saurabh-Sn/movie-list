from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from account.models import User, RequestCount


class RegisterUserSerializer(serializers.ModelSerializer):
    
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        error_messages={
            "blank": "Password cannot be empty.",
            "min_length": "Password too short.",
        },
    )
    username = serializers.CharField(max_length=50)
    
        

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user.exists():
            raise serializers.ValidationError("User with provided username already exists.")
        return value

    class Meta:
        model = User
        fields = [ 'username', 'password', ]

    def create(self, *args, **kwargs):
        user = User.objects.create(
            username=self.validated_data['username'],
            
            password=make_password(self.validated_data['password']),
            is_staff=False,
            

        )
        