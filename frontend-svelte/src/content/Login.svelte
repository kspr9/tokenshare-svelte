<script lang="ts">
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { login } from "../utils/login";

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

    function handleSubmit() {
      login(username, password);
    }

    function closeModal() {
        isLoginModalOpen.set(false);
    }
    
  </script>
  

  {#if $isLoginModalOpen}
    <div class="modal">
        <div class="modal-content">
            <button on:click={closeModal}>Close</button>
            <form on:submit|preventDefault={handleSubmit}>
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