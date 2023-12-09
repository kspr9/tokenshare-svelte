<script lang="ts">
    import { createWorkspace } from "../services/apiServiceForWS";
    import { userData } from "../stores/userDataStore";
    import { get } from 'svelte/store';
    import type { UserProps } from "../types/userProps";
  
    let companyName: string = '';
    let regNumber: number | null = null;
    let maxNumberOfShares: number | null = null;
    let workspaceName: string = '';
    let workspaceDescription: string = '';
    let governanceType: 'Business' | 'Personal' = 'Business';
    let responseMessage: string = '';
    let errorMessage: string = '';
  
    const handleSubmit = async () => {
      try {
        const workspaceOwner: UserProps | null = get(userData);
        if (!workspaceOwner) throw new Error("Session user not found.");
  
        const companyDetails = { companyName, regNumber, maxNumberOfShares };
        const workspaceDetails = { workspaceName, workspaceDescription, workspaceOwner: workspaceOwner.pk };
        const contractDetails = { governanceType };
  
        const formData = new FormData();
        formData.append('companyDetails', JSON.stringify(companyDetails));
        formData.append('workspaceDetails', JSON.stringify(workspaceDetails));
        formData.append('contractDetails', JSON.stringify(contractDetails));
  
        const response = await createWorkspace(formData);
        responseMessage = response.message;
      } catch (error) {
        
      }
    };
  </script>

<form on:submit|preventDefault={handleSubmit}>
    <div class="form-section">
      <h2>Company Details</h2>
      <label for="companyName">Name:</label>
      <input type="text" id="companyName" bind:value={companyName} maxlength="255" />
  
      <label for="regNumber">Registration Number:</label>
      <input type="number" id="regNumber" bind:value={regNumber} />
  
      <label for="maxNumberOfShares">Max Number of Shares:</label>
      <input type="number" id="maxNumberOfShares" bind:value={maxNumberOfShares} />
    </div>
  
    <div class="form-section">
      <h2>Workspace Details</h2>
      <label for="workspaceName">Name:</label>
      <input type="text" id="workspaceName" bind:value={workspaceName} />
  
      <label for="workspaceDescription">Description:</label>
      <textarea id="workspaceDescription" bind:value={workspaceDescription}></textarea>
    </div>
  
    <div class="form-section">
      <h2>Governance Contract Details</h2>
      <label for="governanceType">Type:</label>
      <select id="governanceType" bind:value={governanceType}>
        <option value="Business">Business</option>
        <option value="Personal">Personal</option>
      </select>
    </div>
  
    {#if responseMessage}
      <div class="response-message">{responseMessage}</div>
    {/if}
  
    {#if errorMessage}
      <div class="error-message">{errorMessage}</div>
    {/if}
  
    <button type="submit">Create Workspace</button>
  </form>
  
  <style>
    .form-section {
      margin-bottom: 20px;
    }
  
    label {
      display: block;
      margin: 10px 0 5px;
    }
  
    input, select, textarea {
      width: 100%;
      padding: 8px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  
    .response-message, .error-message {
      margin-top: 20px;
      padding: 10px;
      border-radius: 4px;
    }
  
    .response-message {
      background-color: #dff0d8;
      color: #3c763d;
    }
  
    .error-message {
      background-color: #f2dede;
      color: #a94442;
    }
  
    button {
      padding: 10px 20px;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #45a049;
    }
  </style>