
// utils import
import { navigate } from 'svelte-routing';
import { getCookie } from '../utils/cookie';

// store imports
import { workspaces } from '../stores/workspacesStore';
import { companies } from '../stores/companiesStore';

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
    console.error('Error fetching workspaces:', error);
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
    console.error('Error fetching company data:', error);
  }
}