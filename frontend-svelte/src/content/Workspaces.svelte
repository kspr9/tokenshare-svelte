<script lang="ts">
    import { Link } from "svelte-routing";
    import { onMount } from "svelte";
    import { get, type Writable } from 'svelte/store';

    import WorkspaceCard from "../components/WorkspaceCard.svelte";

    //import { workspaces } from "../stores/workspacesStore";
    //import { companies } from "../stores/companiesStore";
    //import { contracts } from '../stores/contractsStore';

    import { companies, workspaces, contracts } from '../stores/governanceStore';
    import type { Company, Workspace, Contract } from '../types/governanceTypes';


    import {
        APIService,
        fetchCompanies,
        fetchContracts,
        fetchWorkspaces,
    } from "../services/apiServiceForWS";

    // Find the company name
    function company(governorCompanyId: number) {
        const company = $companies.find((c) => c.id === governorCompanyId);
        return company;
    }

    let workspaceDataAvailable: boolean = false;
    let fetchPromise;

    onMount(async () => {
        const apiService = new APIService();
        let workspacesPromise;
        let companiesPromise;
        let contractsPromise;

        if ($workspaces === undefined || $workspaces === null || $workspaces.length === 0) {
            workspacesPromise = apiService.fetchWorkspaces()
            .then((data) => {
                workspaces.set(data);
            })
        }

        if ($companies === undefined || $companies === null || $companies.length === 0) {
            companiesPromise = apiService.fetchCompanies()
            .then((data) => {
                companies.set(data);
            });
        }

        if ($contracts === undefined || $contracts === null || $contracts.length === 0) {
            contractsPromise = apiService.fetchContracts()
            .then((data) => {
                contracts.set(data);
            });
        }

        fetchPromise = Promise.all([workspacesPromise, companiesPromise, contractsPromise])
        .then(() => {
            workspaceDataAvailable = true;
        }).catch(error => {
            console.error("Error resolving fetch promises:", error);
        });
        // Function to fetch and update a store
        /*
        
        function fetchData<T>(fetchFunction: () => Promise<T>, store: Writable<T[]>) {
            const storeValue = get(store);
            if (!storeValue || storeValue.length === 0) {
                return fetchFunction().then(data => {
                    store.set([data]);
                    return data; // return the data for await block
                });
            }
            return Promise.resolve(storeValue);
        }

        // Fetch data for each store
        fetchData<Workspace>(apiService.fetchWorkspaces, workspaces);
        fetchData<Company>(apiService.fetchCompanies, companies);
        fetchData<Contract>(apiService.fetchContracts, contracts);
        */
    });
</script>

<div class="ws-container">
    <h1>Workspaces</h1>


    <div class="ws-items-container">
        {#if workspaceDataAvailable}
            {#each $workspaces as workspace}
                <div class="workspace-item">
                    <WorkspaceCard 
                        workspace={workspace} 
                        company={company(workspace.ws_governor_company)} 
                    />
                </div>
            {/each}
        {:else}
            <p>Loading...</p>
        {/if}

        
        <div class="workspace-add">
            <!-- svelte-ignore a11y-invalid-attribute -->
            <Link to="/app/createWS"><div class="icon-plus app-clr"></div></Link>
        </div>
    </div>
</div>
<style>
    .ws-container {
        width: 80vw;
    }
    .ws-items-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        padding: 20px;
        
    }
    .workspace-add {
        background-color: #333;
        width: 35ch;
        padding: 2ch 0;
        border-radius: 5px;
    }
    

    .workspace-item > a {
        position: relative;
        top: 0.5ch;
        left: 2.5ch;
    }
    .workspace-item:has(a):hover {
        border: #646cff solid 1px;
    }


    /* Plus Icon styling */
    .icon-plus {
        width: 47px;
        height: 47px;
    
        &.w25 {
            width: 25px;
            height: 25px;
            
            border-radius: 5px;
            
            &:after {
                width: 18px;
                height: 4px;
                left: 4px;
                top: 11px;
            }

            &:before {
                width: 4px;
                height: 18px;
                left: 11px;
                top: 4px;
            }
        }
        
        border-radius: 50px;
        
        position: relative;

        &.orange {
            background: #FD7901;
        }
        
        &.blue {
            background: #3498db;
        }

        &.app-clr {
            background: #333;
        }
        
        &:after, &:before {
            content: '';
            position: absolute;
            background: #646cff;
            -webkit-border-radius: 5px;
            -moz-border-radius: 5px;
            border-radius: 5px;
        }

        /* the vertical line */
        &:before {
            left:50%;
            top:4px; /* this defines how much black "border" there should be */
            bottom:4px;
            width:5px;
            transform:translateX(-50%);
        }

        /* the horizontal line */
        &:after {
            top:50%;
            left:4px;
            right:4px;
            height:5px;
            transform:translateY(-50%);
        }
        
    }


    
    
/* END Plus Icon styling */
</style>