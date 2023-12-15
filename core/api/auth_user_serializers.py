from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db import transaction

from core.api.serializers import CompanyRoleSerializer, WorkspaceSerializer
from core.governance.models import Workspace

User = get_user_model()

'''
        username
        first_name
        last_name
        email
        user_wallet_address = models.CharField(max_length=255, unique=True, null=True, blank=True)
            
        through other models
            'owned_workspace' from Workspace model
            'member_in_workspaces' from Workspace model
            'role_in_company' from CompanyRole model
    '''

class SuperuserUserSerializer(serializers.ModelSerializer):
    owned_workspace = WorkspaceSerializer(many=True, read_only=True)
    member_in_workspaces = WorkspaceSerializer(many=True, read_only=True)
    role_in_company = CompanyRoleSerializer(many=True, read_only=True)
    class Meta:
        model = User
        # List all the fields you want the superuser to be able to interact with
        fields = ('id', 
                  'username', 
                  'first_name', 
                  'last_name', 
                  'email', 
                  'is_staff', 
                  'is_active', 
                  'is_superuser', 
                  'last_login', 
                  'date_joined', 
                  #'groups', 
                  #'user_permissions',
                  'user_wallet_address',
                  'owned_workspace',
                  'member_in_workspaces',
                  'role_in_company',
                  )
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only for security
        }

    def create(self, validated_data):
        with transaction.atomic():  # Ensures atomicity of the user creation process
            # Pop related workspace data out of validated_data
            owned_workspace_data = validated_data.pop('owned_workspace', None)
            member_in_workspaces_data = validated_data.pop('member_in_workspaces', [])

            # Create the user
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data.pop('password', None),  # Assuming password is provided
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                is_staff=validated_data.get('is_staff', False),
                is_active=validated_data.get('is_active', True),
                is_superuser=validated_data.get('is_superuser', False),
                user_wallet_address=validated_data.get('user_wallet_address', '')
            )

            # Handle adding the user to member workspaces
            for workspace_data in member_in_workspaces_data:
                workspace_id = workspace_data.get('id')
                if workspace_id:
                    workspace = Workspace.objects.get(id=workspace_id)
                    workspace.workspace_members.add(user)
                    workspace.save()
            
            return user

    def update(self, instance, validated_data):
        with transaction.atomic():  # Ensures atomicity of the update process
            # Pop related workspace membership data out of validated_data
            member_in_workspaces_data = validated_data.pop('member_in_workspaces', None)

            # Update user fields
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.is_staff = validated_data.get('is_staff', instance.is_staff)
            instance.is_active = validated_data.get('is_active', instance.is_active)
            instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
            instance.user_wallet_address = validated_data.get('user_wallet_address', instance.user_wallet_address)
            
            # Handle password update (if provided)
            password = validated_data.get('password')
            if password:
                instance.set_password(password)
            
            instance.save()

            # Update workspace memberships if provided
            if member_in_workspaces_data is not None:
                # Clear existing memberships
                instance.workspace_set.clear()

                # Add new memberships
                for workspace_data in member_in_workspaces_data:
                    workspace_id = workspace_data.get('id')
                    if workspace_id:
                        workspace = Workspace.objects.get(id=workspace_id)
                        workspace.workspace_members.add(instance)
                        workspace.save()
                instance.save()

            return instance
