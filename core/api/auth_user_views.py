
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer

from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .serializers import LoginSerializer, RegisterSerializer

from django.contrib.auth import get_user_model

## TODO Separate views into individual files, such as auth_user_views, governance_views etc

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

#@csrf_exempt
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
                is_authenticated = request.user.is_authenticated
                return Response({'status': 'success', 'message': 'Login successful', 'is_authenticated': is_authenticated})
            else:
                return Response({'status': 'error', 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        is_authenticated = request.user.is_authenticated
        return Response({'status': 'success', 'message': 'Logged out successfully', 'is_authenticated': is_authenticated})


class RegisterAPIView(APIView):
    '''
    APIView for registering a new user.
    Using RegisterSerializer to validate and create the new user.
    '''
    '''
    Preferred this APIView, instead of generics.CreateAPIView because later want to add custom logic.
    
    Some examples where we might use custom logic in our Django Rest Framework views:
        --> Email Verification: After a user registers, you might want to send a verification email. In the custom view, you can add logic to generate a verification token and send an email with a verification link.
        --> Wallets/Contracts? --> Third-Party Integrations: Suppose your user registration needs to interact with external services, like a payment gateway or a CRM system. You could add the logic to create a corresponding customer record in those systems after the user is created in your database.
        --> Deploying Contract, creating Wallets, etc -->  Integration with Background Tasks: For operations that don't need to be completed immediately (like sending welcome emails or processing data for new users), you might enqueue these tasks as background jobs to improve API response times.
        Custom User Logging or Analytics: For detailed logging (e.g., who is registering, when, and from where), you might want to add custom logging logic to record this information either in your database or in an external analytics service.
        Role or Permission Assignment: If your application has complex role-based access control, you might need to assign roles or permissions to the user upon registration, possibly based on the information they provide during signup.
        Complex Validation Logic: While serializers handle basic validation, you might have more complex validation rules that depend on multiple fields or external factors. For example, checking if the user's age is appropriate based on their country's legal requirements.
        Custom Response Data: You might want to return a custom response structure that includes additional data beyond what the serializer provides, such as tokens for API access, links to user guides, or personalized welcome messages.
        Rate Limiting or Anti-Spam Measures: Implement custom checks to prevent abuse of the registration endpoint, such as limiting the number of accounts created from the same IP address in a short period.
        Data Transformation: In some cases, you might need to transform request data before it's serialized or transform serialized data before it's returned in the response.
        Custom Authentication or Token Generation: You might need to implement a custom authentication mechanism or token generation logic as part of the registration process, especially if your application uses a non-standard way of handling user sessions or security tokens.
    '''
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
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