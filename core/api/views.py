from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer

from django.contrib.auth import get_user_model


class GreetingApi(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        return Response({"message": "Hello world"})

class AuthUserApi(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user = request.user
        is_signed_in = user.is_authenticated

        if is_signed_in:
            # Accessing user model fields like username or other fields
            user_data = {
                'username': user.username,
                # Add other user model fields here as needed
                # 'email': user.email,
                # 'first_name': user.first_name,
                # 'last_name': user.last_name,
                # etc.
            }
        else:
            user_data = {}

        response_data = {
            'isSignedIn': is_signed_in,
            'userData': user_data,
            'message': 'Auth check completed'
        }

        return Response(response_data)