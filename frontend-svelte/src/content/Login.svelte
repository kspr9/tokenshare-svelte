<script lang="ts">
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { isAuthenticated } from "../stores/isAuthenticatedStore";

    let username: string | any = '';
    let password: string | any = '';
    let errorMessage: string | any = '';
    
    let csrfToken: string | any;
    

    onMount(async () => {
        csrfToken = getCookie('csrftoken');
    });

    async function login() {
      try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();

        if (!response.ok) {
            errorMessage = data.message;
            throw new Error(errorMessage);
        };

        // Update the isAuthenticated state.
        isAuthenticated.set(data.is_authenticated);
        navigate("/app/dashboard", { replace: true });

      } catch (error) {
        console.error('Login unsuccessful in catch:', error);
        errorMessage = (error as Error).message;
        throw error;
      }
    }

    function getCookie(name: string) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
  </script>
  
  <form on:submit|preventDefault={login}>
    <input type="text" bind:value={username} placeholder="Username">
    <input type="password" bind:value={password} placeholder="Password">
    <input type='hidden' name='csrfmiddlewaretoken' value={csrfToken}>
    <button type="submit">Login</button>
    {#if errorMessage}
      <p>{errorMessage}</p>
    {/if}
  </form>
  