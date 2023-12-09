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


from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

## Models import
from core.accounts.models import User
from ..governance.models import Workspace, Company, GovernanceContract

## Serializers import
from .serializers import WorkspaceSerializer, CompanySerializer, GovernanceContractSerializer, WorkspaceCompanyContractSerializer

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        """
        This view returns a list of all the workspaces
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            return Workspace.objects.filter(workspace_owner=user)
        return Workspace.objects.none()

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

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