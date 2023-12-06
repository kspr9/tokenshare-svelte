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

def create_workspace(company_details, workspace_details, admin_address, gov_type='Business'):
    '''
        Company details: (
            name<string> - from proxy model
            reg_number<int>, 
            max_number_of_shares<int>,
        )
        Workspace details: (
            workspace_name<string>, 
            workspace_description<string>, 
            workspace_logo - optional, 
            workspace_owner (session user), 
            ws_governor_contract<string> - None, intially (will be created during process), 
        )
    '''
    created_company = create_company(company_details, admin_address, gov_type)
    workspace = Workspace(
        workspace_name=workspace_details.get('workspace_name'),
        workspace_decription=workspace_details.get('workspace_description'),
        workspace_owner=workspace_details.get('workspace_owner'),
        ws_governor_contract=created_company.governing_contract
    )
    workspace.save()
    return workspace

def create_company(data, admin_address, gov_type='Business'):
    """
    Create a Company instance from a data dictionary.

    :param data: Dictionary containing company data (
        name<string>,
        reg_number<int>,  
        max_number_of_shares<int>,
        governing_contract<string> - optional
        )
    :param admin_address<string>: The admin address of the governance contract.
    :param gov_type<string>: The type of governance contract. - optional, default Business
    :return: .
    """
    # Extracting data
    reg_number = data.get('reg_number')
    max_number_of_shares = data.get('max_number_of_shares')
    governing_contract = create_governance_contract(data, admin_address, gov_type)

    # Create the Company instance
    company = Company(
        reg_number=reg_number,
        max_number_of_shares=max_number_of_shares,
        governing_contract=governing_contract
    )
    company.save()

    return company

def create_governance_contract(contract_params, admin_address, governance_type='Business'):
    # create GovernanceContract instance
    valid_types = [choice[0] for choice in GovernanceContract.CONTRACT_CHOICES]
    if governance_type not in valid_types:
        raise ValueError(f"Invalid governance type. Must be one of: {valid_types}")

    # Create the GovernanceContract instance without contract_address
    contract = GovernanceContract(
        governance_type=governance_type,
        admin_address=admin_address,
    )
    contract.save()
    # deploy contract as per params
    deployed_contract_address = deploy_governance_contract(contract_params, contract.admin_address)
    # update GovernanceContract instance with contract address
    contract.contract_address = deployed_contract_address
    contract.save()
    return contract

def deploy_governance_contract(contract_params, admin_address):
    '''
        Company details: (
            name<string> - from proxy model
            reg_number<int>, 
            max_number_of_shares<int>,
        )
    '''
    deployable_data = {
        'admin_address': admin_address,
        'reg_number': contract_params.get('reg_number'),
        'max_number_of_shares': contract_params.get('max_number_of_shares'),
    }
    def deploy_gov_contract(deployable_data):
        return input('Which address to use for DEMO process?: ')

    contract_address = deploy_gov_contract(deployable_data)
    
    return contract_address



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
C1 = create_company(company_data1)

C2 = create_company(company_data2)         

C3 = create_company(company_data3)



WS1 = create_workspace(company_data1, ws_data1, kspr.user_wallet_address, gov_type='Business')