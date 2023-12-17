
export interface Company {
    id: number
    name: string
    company_type: string
    reg_number: number | null
    max_number_of_shares: number | null
}

export interface Workspace {
    id: number
    workspace_name: string
    workspace_description: string
    workspace_owner: number
    ws_governor_company: number
    workspace_members: number[]; // Array of user primary keys
}

export interface Contract {
    id: number
    governance_type: string
    contract_address: string
    admin_address: string
    governed_company: number
}