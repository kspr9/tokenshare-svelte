
// utils import
import { navigate } from 'svelte-routing';
import { getCookie } from '../utils/cookie';

// store imports
import { workspaces } from '../stores/workspacesStore';
import { companies } from '../stores/companiesStore';
import { contracts } from '../stores/contractsStore';

let csrfToken: string | any;

csrfToken = getCookie('csrftoken');

export const createWorkspace = async (requestBody: any): Promise<any> => {
  try {
    console.log(requestBody);
    const response = await fetch('/api/companies/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(requestBody),
    });

    const data = await response.json();

    if (!response.ok) {
      console.log("Create WS not ok Data:", data);
      throw new Error('Network response was not ok');
    }
    console.log("Success Data:", data);
    navigate("/app/workspaces", { replace: true });
    return data;

  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    throw new Error('Failed to create workspace');
  }
};



export class APIService {

  fetchWorkspaces = () => {
    return this.apiFetch('/api/workspaces/');
  }

  fetchCompanies = () => {
    return this.apiFetch('/api/companies/');
  }

  fetchContracts = () => {
    return this.apiFetch('/api/contracts/');
  }

  async apiFetch(endpoint: string) {
    try {

      const response = await fetch(endpoint, {
        method: 'GET', 
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken  
        }
      });

      const data = await response.json();

      if (!response.ok) {
        console.log(`Fetch Data for ${endpoint} not ok:`, data);
        throw new Error('Network response was not ok');
      }

      console.log(`Success fetching ${endpoint} Data:`, data);

      return data;

    } catch (error) {
      console.error(`Error fetching ${endpoint} data:`, error);
    }
  }
}

export async function fetchWorkspaces() {
  try {
    const response = await fetch('/api/workspaces/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    });

    const data = await response.json();

    if (!response.ok) {
      console.log("Fetch WS not ok Data:", data);
      throw new Error('Network response was not ok');
    }

    console.log("Success fetching WS Data:", data);
    workspaces.set(data);

    return data;

  } catch (error) {
    console.error('Error fetching workspaces data:', error);
  }
}

export async function fetchCompanies() {
  try {
    const response = await fetch('/api/companies/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    });

    const data = await response.json();


    if (!response.ok) {
      console.log("Fetch Company data not ok:", data);
      throw new Error('Network response was not ok');
    }

    console.log("Success fetching Company data:", data);
    companies.set(data);

    return data;

  } catch (error) {
    console.error('Error fetching companies data:', error);
  }
}

export async function fetchContracts() {
  try {
    const response = await fetch('/api/contracts/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      }
    });

    const data = await response.json();

    if (!response.ok) {
      console.log("Fetch Contract data not ok:", data);
      throw new Error('Network response was not ok');
    }

    console.log("Success fetching Contract data:", data);
    contracts.set(data);

    return data;
  } catch (error) {
    console.error('Error fetching contracts data:', error);
  } 
}