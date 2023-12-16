## TODO Separate views into individual files, such as auth_user_views, governance_views etc

'''
    views for:
        Dashboard
            get
        workspaces
            get
        workspace<int:workspace_id> ie workspace detail view
            get (get a workspace + associated gov contract and contract assets (ie companies))
            post (create a new workspace, specify company, deploy contract etc)
        settings
            get
            update
        profile
            get
            update
        company
            get
            post
            update
        contract
            get
            post
            update
'''


from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

## Models import
from core.accounts.models import User
from ..governance.models import CompanyRole, Workspace, Company, GovernanceContract

## Serializers import
from .serializers import CompanyRoleSerializer, WorkspaceSerializer, CompanySerializer, GovernanceContractSerializer, WorkspaceCompanyContractSerializer

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    '''
    def get_queryset(self):
        """
        This view returns a list of all the workspaces
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            return Workspace.objects.filter(workspace_owner=user)
        return Workspace.objects.none()
    '''

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    '''
    def get_queryset(self):
        """
        This view returns a list of all the companies
        for the currently authenticated user.
        """
        user = User.objects.get(id=self.request.user.id)
        wallet_address = user.user_wallet_address
        if user.is_authenticated:
            return Company.objects.filter(governing_contract__admin_address=wallet_address)
        return Company.objects.none()
    '''
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Custom logic for creating Workspace and GovernanceContract
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == 201:
            company_id = response.data['id']
            company = Company.objects.get(id=company_id)
            # Retrieve the User instance
            user = get_user_model().objects.get(id=request.user.id)

            # Extract Workspace data from request
            workspace_data = request.data.get('workspace_data', {})
            workspace_data['ws_governor_company'] = company
            workspace_data['workspace_owner'] = user
            Workspace.objects.create(**workspace_data)

            
            # Extract GovernanceContract data from request
            governance_data = request.data.get('governance_contract_data', {})
            governance_data['governed_company'] = company
            # Extract admin address from request, 
            #or default to user wallet address if value missing from the governance_data
            admin_address = governance_data.get('admin_address', request.user.user_wallet_address)
            governance_data['admin_address'] = admin_address
            GovernanceContract.objects.create(**governance_data)
        return response




class GovernanceContractViewSet(viewsets.ModelViewSet):
    queryset = GovernanceContract.objects.all()
    serializer_class = GovernanceContractSerializer


class CreateWorkspaceViewSet(viewsets.ViewSet):
    # Define any standard actions if needed (list, retrieve, etc.)

    @action(detail=False, methods=['post'])
    def create_composite(self, request):
        serializer = WorkspaceCompanyContractSerializer(data=request.data)
        if serializer.is_valid():
            workspace = serializer.save()
            return Response(
                {
                    "workspace": WorkspaceSerializer(workspace).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CompanyRoleViewSet(viewsets.ModelViewSet):
    queryset = CompanyRole.objects.all()
    serializer_class = CompanyRoleSerializer