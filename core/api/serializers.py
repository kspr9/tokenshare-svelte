from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator

from core.governance.models import Company, GovernanceContract, PersonalCompany, Workspace

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

class WorkspaceCompanyContractSerializer(serializers.ModelSerializer):
    pass

class RegisterWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('workspace_name', 'workspace_description', 'workspace_logo')


class RegisterCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'reg_number', 'max_number_of_shares')

class RegisterPersonalCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCompany
        fields = ('name')





class GovernanceContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernanceContract
        fields = ('contract_address', 'admin_address', 'governance_type')

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('workspace_name', 'workspace_description', 'workspace_logo' ,'workspace_owner', 'ws_governor_contract')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'reg_number', 'max_number_of_shares')

class PersonalCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalCompany
        fields = ('name')

