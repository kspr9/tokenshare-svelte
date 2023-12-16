<script lang="ts">
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    

    // Store import
    import { isAuthenticated } from "../stores/isAuthenticatedStore";
    import { isLoginModalOpen } from "../stores/isLoginModalOpenStore";

    // utils import
    import { getCookie } from "../utils/cookie";

    //variable declarations
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

        if (response.ok) {
          isAuthenticated.set(data.is_authenticated);
          navigate("/app/dashboard", { replace: true });
          isLoginModalOpen.set(false); // Close the modal on successful login
        } else {
          // Handle login error
          errorMessage = data.message;
          throw new Error(errorMessage);
        }

      } catch (error) {
        console.error('Login unsuccessful in catch:', error);
        errorMessage = (error as Error).message;
        throw error;
      }
    }

    

    function closeModal() {
        isLoginModalOpen.set(false);
    }
  </script>
  
  <form on:submit|preventDefault={login}>
    
  </form>

  {#if $isLoginModalOpen}
    <div class="modal">
        <div class="modal-content">
            <button on:click={closeModal}>Close</button>
            <form on:submit|preventDefault={login}>
              <input type="text" bind:value={username} placeholder="Username">
              <input type="password" bind:value={password} placeholder="Password">
              <input type='hidden' name='csrfmiddlewaretoken' value={csrfToken}>
              <button type="submit">Login</button>
              {#if errorMessage}
                <p>{errorMessage}</p>
              {/if}
            </form>
        </div>
    </div>
  {/if}
  
  <style>
    .modal {
        display: flex;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;
        background-color: rgba(0, 0, 0, 0.5);
    }
    .modal-content {
        background-color: #333;
        padding: 20px;
        border-radius: 5px;
    }
</style>