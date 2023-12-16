from rest_framework import serializers
from django.db import transaction

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator

from core.governance.models import Company, CompanyRole, CompanyShare, GovernanceContract, Workspace


###                         ###
###     APP SERIALIZERS     ###
###                         ###

## Used for logging in the user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# Used for registering a new user in the app
class RegisterSerializer(serializers.ModelSerializer):
    # Explicitly declare the fields needed for registration
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

#########################################
###     Serializers for registering/creation
###        still deciding if we need these
########################################
class WorkspaceCompanyContractSerializer(serializers.ModelSerializer):
    pass

class CreateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ('workspace_name', 'workspace_description', 'workspace_logo')


class CreateCompanySerializer(serializers.ModelSerializer):
    pass





########################################
### Serializers for interacting with models
########################################
User = get_user_model()

class CompanyShareSerializer(serializers.ModelSerializer):
    holder = serializers.SerializerMethodField()

    class Meta:
        model = CompanyShare
        fields = ['issuing_company', 
                  'shares_amount', 
                  'share_type', 
                  'date_issued',
                  'owning_contract',
                  'date_last_ownership_change',
                  'holder'
        ]
    
    def get_holder(self, obj):
        """
        Returns the contract address of the holder.
        """
        return obj.holder

class CompanyRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRole
        fields = ['user', 'company', 'role_type']
        


class CompanySerializer(serializers.ModelSerializer):
    # Flat serializer for create/update
    class Meta:
        model = Company
        fields = '__all__'

class WorkspaceSerializer(serializers.ModelSerializer):
    # Flat serializer for create/update
    class Meta:
        model = Workspace
        fields = '__all__'

class GovernanceContractSerializer(serializers.ModelSerializer):
    # Flat serializer for create/update
    class Meta:
        model = GovernanceContract
        fields = '__all__'

'''

class GovernanceContractSerializer(serializers.ModelSerializer):
    owned_company_shares = CompanyShareSerializer(many=True, read_only=True)
    governed_company = serializers.SerializerMethodField()
    class Meta:
        model = GovernanceContract
        fields = [ 
                  'governance_type',
                  'contract_address',
                  'admin_address', 
                  'governed_company',
                  'owned_company_shares'
        ]

    def get_governed_company(self, obj):
        from .serializers import CompanySerializer
        if obj.governed_company is not None:
            return CompanySerializer(obj.governed_company).data
        return None

class WorkspaceSerializer(serializers.ModelSerializer):
    workspace_owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
        default=serializers.CurrentUserDefault())
    ws_governor_company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    workspace_members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        company = context.get('company')

        # Modify the queryset based on the passed company instance
        if company:
            self.fields['ws_governor_company'].queryset = Company.objects.filter(id=company.id)
        
        super(WorkspaceSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Workspace
        fields = ['workspace_name', 
                  'workspace_description', 
                  'workspace_logo', 
                  'workspace_owner', 
                  'ws_governor_company', 
                  'workspace_members'
        ]

    
    """
    def get_ws_governor_company(self, obj):
        from .serializers import CompanySerializer
        if obj.ws_governor_company is not None:
            return CompanySerializer(obj.ws_governor_company).data
        return None
    """
    


class CompanySerializer(serializers.ModelSerializer):
    company_workspace = WorkspaceSerializer()
    governing_contract = GovernanceContractSerializer(read_only=True)
    shares_issued = CompanyShareSerializer(many=True, read_only=True)
    company_roles = CompanyRoleSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['company_type', 
                  'name', 
                  'governing_contract', 
                  'reg_number', 
                  'max_number_of_shares', 
                  'company_workspace',
                  'shares_issued',
                  'company_roles'
                ]
    
    # this is to pass context to the WorkspaceSerializer
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        # Pass the company instance as part of the context
        self.fields['company_workspace'] = WorkspaceSerializer(context={'company': instance})
        return super(CompanySerializer, self).to_representation(instance)
    
    

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
    

    def create(self, validated_data):
        
        with transaction.atomic():
            # Extract workspace data from the validated data
            workspace_data = validated_data.pop('company_workspace', None)

            # Create the Company instance
            company = Company.objects.create(**validated_data)

            # Create the Workspace instance, if workspace data is provided
            if workspace_data:
                # extract the user_id assuming workspace_owner provides the id
                owner_id = workspace_data.pop('workspace_owner')
                workspace_owner = User.objects.get(pk=owner_id)

                workspace_data['workspace_owner'] = workspace_owner
                workspace_data['ws_governor_company'] = company  # Set the company as the governor company
                
                Workspace.objects.create(**workspace_data)

            # Return the newly created company instance
            return company


'''
