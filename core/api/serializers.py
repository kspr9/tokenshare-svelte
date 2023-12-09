from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator

from core.governance.models import Company, GovernanceContract, Workspace

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class RegisterSerializer(serializers.ModelSerializer):
    # Explicitly declare the fields you need for registration
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2', 'user_wallet_address')
        extra_kwargs = {
            'username': {'required': True}, 
            'first_name': {'required': True}, 
            'last_name': {'required': True}, 
            'email': {'required': True}, 'validators': [EmailValidator()]}

    def validate(self, data):
        # Check if the two passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data
    
    def create(self, validated_data):
        # Create a new user instance
        user = get_user_model().objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            user_wallet_address=validated_data.get('user_wallet_address')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    '''
        username
        first_name
        last_name
        email
        user_wallet_address = models.CharField(max_length=255, unique=True, null=True, blank=True)
        roles_in_companies = models.ManyToManyField('governance.Company', through='governance.CompanyRoles', related_name='users_with_roles', blank=True)
            
        through other models
            'owned_workspace' from Workspace model
            'member_in_workspaces' from Workspace model
            Company model has governance_contract
            GovernanceContract has 'owned_company_shares' through CompanyShares model
    '''

### Serializers for registering
########################################
class WorkspaceCompanyContractSerializer(serializers.ModelSerializer):
    pass

class RegisterWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('workspace_name', 'workspace_description', 'workspace_logo')


class RegisterCompanySerializer(serializers.ModelSerializer):
    pass





########################################
### Serializers for interacting with models
########################################

class GovernanceContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernanceContract
        fields = ['contract_address', 
                  'admin_address', 
                  'governance_type',
                  'governed_company',
                  'owned_company_shares'
        ]

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['workspace_name', 
                  'workspace_description', 
                  'workspace_logo', 
                  'workspace_owner', 
                  'ws_governor_company', 
                  'workspace_members'
        ]



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_type', 
                  'name', 
                  'governing_contract', 
                  'reg_number', 
                  'max_number_of_shares', 
                  'company_workspace',
                  'shares_issued',
                  'company_roles']

    def validate(self, data):
        company_type = data.get('company_type')

        errors = {}
        if company_type == 'Business':
            if data.get('reg_number') is None:
                errors['reg_number'] = 'This field is required for Business type.'
            if data.get('max_number_of_shares') is None:
                errors['max_number_of_shares'] = 'This field is required for Business type.'
        
        elif company_type == 'Personal':
            if data.get('reg_number') is not None:
                errors['reg_number'] = 'This field should not be provided for Personal type.'
            if data.get('max_number_of_shares') is not None:
                errors['max_number_of_shares'] = 'This field should not be provided for Personal type.'

        if errors:
            raise serializers.ValidationError(errors)

        return data

