from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Author, Submission

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Author

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    firstname = serializers.CharField(write_only=True)
    lastname = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Author
        fields = ['username', 'firstname', 'lastname', 'password', 'email']

    def validate_username(self, value):
        # Check if the username already exists
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        # Check if the email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken.")
        return value

    def create(self, validated_data):
        # Create the User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['firstname'],
            last_name=validated_data['lastname'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        # Create the Author instance linked to the User
        author = Author.objects.create(user=user)
        return author



class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'author', 'title', 'description', 'file', 'created_at']
        read_only_fields = ['id', 'created_at', 'author']  # Author is set automatically
