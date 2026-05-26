from django.contrib.auth import authenticate
from auth_app.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserMinimalSerializer(serializers.ModelSerializer):
    """
    Serializer for low-overhead user data representation.

    Primarily used when listing users or embedding public user data
    inside other nested API responses without exposing sensitive fields.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user accounts during registration and
    detailed profiles.

    Includes password validation logic and automatically attaches
    an authentication token upon successful creation.
    """
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ['token', 'fullname', 'email',
                  'user_id', 'password', 'repeated_password']

    def get_token(self, obj):
        """
        Dynamic lookup to fetch the user's authentication token.

        Args:
            obj (User): The user instance being serialized.

        Returns:
            str/None: The token key if it exists, otherwise None.
        """
        token = Token.objects.filter(user=obj).first()
        return token.key if token else None

    def validate(self, data):
        """
        Validates that both submitted passwords match exactly.

        Args:
            data (dict): The dictionary of incoming request data.

        Raises:
            ValidationError: If the password and repeated_password do not
             match.

        Returns:
            dict: The validated data.
        """
        if data.get('password') != data.get('repeated_password'):
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Creates a new User instance and provisions an API Auth Token.

        Args:
            validated_data (dict): Cleaned and validated dictionary from the
             request.

        Returns:
            User: The newly created and saved user instance.
        """
        validated_data.pop('repeated_password')
        user = User.objects.create_user(
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Validates that the provided email and password match an existing user
    and returns the authenticated user instance.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        """
        Validates the incoming login data by authenticating the user.

        Args:
            attrs (dict): A dictionary of field values passed to the
            serializer.

        Raises:
            serializers.ValidationError: If both email and password are not
            provided,or if authentication fails due to invalid credentials.

        Returns:
            dict: The validated attributes, including the authenticated
            'user' object.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    {"non_field_errors": [
                        "Unable to log in with provided credentials."]},
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                {"non_field_errors": ["Must include 'email' and 'password'."]},
                code='authorization'
            )
        attrs['user'] = user
        return attrs
