from .serializers import UserSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    """
    API endpoint that allows new users to register an account.

    Permissions:
        - AllowAny (Publicly accessible)

    Methods:
        - POST: Validates payload, creates user, generates a token,
          returns the profile.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests for user registration.

        Expected JSON Body:
            {
                "fullname": "John Doe",
                "email": "john@example.com",
                "password": "secure123",
                "repeated_password": "secure123"
            }
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'fullname': user.fullname,
                    'email': user.email,
                    'user_id': user.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    """
    API endpoint for user authentication using token-based auth.

    Permissions:
        - AllowAny (Publicly accessible)

    Methods:
        - POST: Validates credentials, fetches/creates a permanent token,
                and returns basic user details alongside the token.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handles POST requests for user login.

        Expected JSON Body:
            {
                "email": "john@example.com",
                "password": "secure123"
            }
        """
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'fullname': user.fullname,
                'email': user.email,
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
