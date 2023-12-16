

export interface Workspace {
    id: number
    workspace_name: string
    workspace_description: string
    workspace_owner: number
    ws_governor_company: number
    workspace_members: number[]; // Array of user primary keys
}