from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer

from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer

from django.contrib.auth import get_user_model



@api_view(['GET'])
def check_authentication_status(request):
    """
        Check the authentication status of a request.

        :param request: The request object.
        :type request: HttpRequest
        :return: A Response object containing the authentication status.
        :rtype: Response
    """
    is_authenticated = request.user.is_authenticated
    return Response({'is_authenticated': is_authenticated})


class GreetingApi(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        return Response({"message": "Hello world"})


class LoginAPIView(APIView):
    """
        Handles the HTTP POST request for logging in a user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the login status and message.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'status': 'success', 'message': 'Login successful'})
            else:
                return Response({'status': 'error', 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthUserApi(APIView):    
    """
        Retrieves the user data and authentication status.

        Parameters:
            request (HttpRequest): The HTTP request object.
            format (str, optional): The format of the response data. Defaults to None.

        Returns:
            Response: The response object containing the user data and authentication status.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user = request.user
        is_signed_in = user.is_authenticated

        if is_signed_in:
            # Accessing user model fields like username or other fields
            user_data = {
                'pk': user.pk,  # Primary key of the user
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        else:
            user_data = {}

        response_data = {
            'isSignedIn': is_signed_in,
            'userData': user_data,
            'message': 'Auth check completed'
        }

        return Response(response_data)