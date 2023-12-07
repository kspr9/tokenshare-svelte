
from typing import Dict
from django.db import transaction
from .utils import validate_data, log_error

from core.accounts.models import User
from core.governance.models import (Company,
                                    PersonalCompany,
                                    GovernanceContract,
                                    Workspace, 
                                    CompanyRoles,
                                    CompanyShares,
                                    TimelineEvent,
                                    )

# In Dashboard - user clicks to create a Workspace
# Either a Personal Company or a Business Company
#
# Create workspaces governor that: 
# Has a 'Governor Wallet' that does not issue shares (although could)
# Owns shares in other companies
'''
    Process:
    In the dashboard, user clicks -> create a company (or a workspace)
    User is directed to create a company form
        Data: reg#, Company Name, Max shares, 
        This data is used to 
            a) deploy a covernance contract with
                data of the company
                users wallet address as admin address of the contract
                select contract type: business or personal
        WAIT until the contract is deployed and contract address is received
        Once governance contract address is available, create the Company instance

        Once Company instance is created, create a Workspace
            Data: 
                Name of the workspace
                Description
                upload a logo
                Set User as the owner of the workspace
                set Governance Contract address as ws_governor_contract
                leave assets blank
                option to add members to workspace - can be added later
        Once Workspace is created, display success message, and navigate to Workspace dashboard

        OPTION2
            In the dashboard, user clicks -> create a workspace
            User is directed to create a workspace form
            User selects to create either a personal or business workspace

            if Business, then user is presented to enter 'company details' as well as 'workspace details'
            if Personal, then user is presented to enter personal workspace details

            BUSINESS:
                Company details: (
                    name<string> - from proxy model
                    reg_number<int>, 
                    max_number_of_shares<int>,
                )
                Workspace details: (
                    workspace_name, 
                    workspace_description, 
                    workspace_logo - optional, 
                    workspace_owner (session user), 
                    ws_governor_contract (will be created during process), 
                )
                GovernanceContract details: (
                    contract_address - to be received once deployed,
                    admin_address - Users wallet address,
                    governance_type - Business
                )
            PERSONAL:
                Company details: (
                    name<string>
                )
                Workspace details: (
                    workspace_name, 
                    workspace_description, 
                    workspace_logo - optional, 
                    workspace_owner (session user), 
                    ws_governor_contract (will be created during process), 
                )
                GovernanceContract details: (
                    contract_address - to be received once deployed,
                    admin_address - Users wallet address,
                    governance_type - Personal
                )


'''

# Process Description for Creating a Workspace:
# This process involves creating either a personal or a business workspace.
# It includes the creation of a company, governance contract, and workspace,
# with the user initiating the process through the dashboard.

def create_workspace(company_details: Dict[str, object], workspace_details: Dict[str, object], user: User, gov_type: str = 'Business') -> Workspace:
    """
    Create a workspace and an associated company.

    This function first creates a company with the provided details, admin address, and governance type.
        Creating a company includes deploying a governance contract that is used to govern the company and the workspace.
    Then, it creates a workspace linked to this company.

    Parameters:
    - company_details (dict): Details of the company, 
        ['name', 'reg_number', 'max_number_of_shares']
    - workspace_details (dict): Details of the workspace,
        ['workspace_name', 'workspace_description' - optional, 'workspace_owner': User]
    - user (User): Administrator address for the governance contract.
    - gov_type (str, optional): Type of governance, defaults to 'Business'.

    Returns:
    Workspace: The newly created workspace instance.
    """

    try:
        # Validate required company details
        if not validate_data(company_details, ['name', 'reg_number', 'max_number_of_shares']):
            log_error("Invalid company details", company_details)
            raise ValueError("Missing required company details")

        # Validate required workspace details - 'workspace_description' is optional
        if not validate_data(workspace_details, ['workspace_name', 'workspace_owner']):
            log_error("Invalid workspace details", workspace_details)
            raise ValueError("Missing required workspace details")

        with transaction.atomic():
            # Creating a company
            created_company = create_company(company_details, user.user_wallet_address, gov_type)

            # Creating a workspace
            workspace = Workspace.objects.create(
                workspace_name=workspace_details.get('workspace_name'),
                workspace_description=workspace_details.get('workspace_description'),
                workspace_owner=user,
                ws_governor_contract=created_company.governing_contract
            )

        return workspace

    except Exception as e:
        # Log the exception or handle it appropriately
        # For example, using logging.error(e) or similar approach
        '''
        Specific Exceptions: Catching general exceptions (Exception) is a broad approach. 
            It's usually better to catch specific exceptions 
            (like ValueError, IntegrityError from Django ORM, etc.) where possible.
        '''
        raise ValueError(f"Error creating workspace: {str(e)}")

def create_company(data: Dict[str, object], admin_address: str, gov_type: str = 'Business') -> Company:
    """
    Create a Company instance from provided data.

    Parameters:
    - data (dict): Dictionary containing company data like name, registration number, and max shares.
    - admin_address (str): The admin address of the governance contract.
    - gov_type (str, optional): The type of governance contract, defaults to 'Business'.

    Returns:
    Company: The newly created company instance.
    """

    try:
        if 'reg_number' not in data or 'max_number_of_shares' not in data:
            log_error("Invalid company data", data)
            raise ValueError("Missing required company data while creating a company")

        # Extracting company data from the provided dictionary
        name = data.get('name')
        reg_number = data.get('reg_number')
        max_number_of_shares = data.get('max_number_of_shares')

        with transaction.atomic():
            governing_contract = create_governance_contract(data, admin_address, gov_type)

            # Creating and saving the Company instance
            company = Company.objects.create(
                name=name,
                reg_number=reg_number,
                max_number_of_shares=max_number_of_shares,
                governing_contract=governing_contract
            )

        return company
    
    except Exception as e:
        # Log the exception, or handle it appropriately
        raise ValueError(f"Error creating company: {str(e)}")

def create_governance_contract(contract_params: Dict[str, object], admin_address: str, governance_type: str = 'Business') -> GovernanceContract:
    """
    Create a GovernanceContract instance.

    This function creates a GovernanceContract instance and deploys the contract based on the provided parameters.
    It validates the governance type and throws an error for invalid types.

    Parameters:
    - contract_params (dict): Parameters for contract creation.
    - admin_address (str): Administrator address for the contract.
    - governance_type (str, optional): Type of governance contract, defaults to 'Business'.

    Returns:
    GovernanceContract: The newly created and deployed governance contract instance.
    """
    try:
        # Validation of governance type
        valid_types = [choice[0] for choice in GovernanceContract.CONTRACT_CHOICES]

        if governance_type not in valid_types:
            log_error("Invalid governance type", governance_type)
            raise ValueError(f"Invalid governance type. Must be one of: {valid_types}")

        with transaction.atomic():
            # Creating the GovernanceContract instance without a contract address
            contract = GovernanceContract.objects.create(
                governance_type=governance_type,
                admin_address=admin_address,
            )

            # Deploying the governance contract and updating the instance with the contract address
            deployed_contract_address = deploy_governance_contract(contract_params, contract.admin_address)
            contract.contract_address = deployed_contract_address
            contract.save()
        return contract
    except Exception as e:
        # Log the exception, or handle it appropriately
        raise ValueError(f"Error creating governance contract: {str(e)}")

def deploy_governance_contract(contract_params: Dict[str, object], admin_address: str) -> str:
    """
    Deploy a governance contract.

    This function is a placeholder for the actual deployment logic of the governance contract.
    Currently, it simulates the deployment process.

    Parameters:
    - contract_params (dict): Parameters for the contract deployment.
    - admin_address (str): Administrator address for the contract.

    Returns:
    str: The address of the deployed contract (simulated for now).
    """

    try:
        if not validate_data(contract_params, ['reg_number', 'max_number_of_shares']):
            log_error("Missing required parameters for contract deployment", contract_params)
            raise ValueError("Missing required parameters for contract deployment")
    
        deployable_data = {
            'admin_address': admin_address,
            'reg_number': contract_params.get('reg_number'),
            'max_number_of_shares': contract_params.get('max_number_of_shares'),
        }

        def deploy_gov_contract(deployable_data):
            # TODO: Implement actual deployment logic
            # the proper way might be to create objects (company + workspace)
            # but then the frontend should deploy the contract?
            # or maybe it would still be the backend?
            return input('Which address to use for DEMO process?: ')

        contract_address = deploy_gov_contract(deployable_data)
        
        return contract_address
    
    except Exception as e:
        # Log the exception, or handle it appropriately
        log_error("Error deploying governance contract", str(e), f"{contract_params=}", f"{admin_address=}")
        raise ValueError(f"Error deploying a governance contract: {str(e)}")


####################
#### DEMO DATA #####
####################
#kaspar = User.objects.get(username='kaspar')
kspr = User.objects.get(username='kspr')
miku5 = User.objects.get(username='miku5')



company_data1 = {
    'name': 'TokenInvest',
    'reg_number': 654321,
    'max_number_of_shares': 250,
    'governing_contract': None  # 
}

company_data2 = {
    'name': "Miku's Miracles LLC",
    'reg_number': 123456,
    'max_number_of_shares': 1000,
    'governing_contract': None  # 
}

company_data3 = {
    'name': 'Testing Company',
    'reg_number': 546231,
    'max_number_of_shares': 100_000,
    'governing_contract': None  # 
}

ws_data1 = {
    'workspace_name': 'TokenInvest',
    'workspace_description': 'The TokenInvest workspace',
    'workspace_owner': kspr,
}
ws_data2 = {
    'workspace_name': "Miku's Miracles LLC",
    'workspace_description': 'I manage my miracle investments here',
    'workspace_owner': miku5,
}
ws_data3 = {
    'workspace_name': 'Testing Workspace',
    'workspace_description': 'Workspace for testing purposes',
    'workspace_owner': kspr,
}

governor_wallet1 = 'KT1LrQT85FnJrMxhq3sCiTbZmru75g7dPiHB'
governor_wallet2 = 'KT1GBr99aBEDovV7dUnnS2QrCqAewp9jSeHK'
governor_wallet3 = 'KT1AoXwHX3YiaM6Pcuc5fvb6YMj8AMvBVVhP'

wallet1 = 'tz1RuTC6e6FxWLTPPjAG3tesiBwwkK1bBkqR'
wallet2 = 'tz1QSURdw5fx5E24q2LGcPmiekyP38L3GpXf'


##########################
### TESTING FUNCTIONS ####
##########################
#C1 = create_company(company_data1)

#C2 = create_company(company_data2)         

#C3 = create_company(company_data3)

#WS1 = create_workspace(company_data1, ws_data1, kspr, gov_type='Business')