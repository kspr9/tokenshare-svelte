<script lang="ts">
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
  
    let username: string | any = '';
    let firstName: string | any = '';
    let lastName: string | any = '';
    let email: string | any = '';
    let password: string | any = '';
    let confirmPassword: string | any = '';
    let userWalletAddress: string | any = ''; 

    let errorMessage: string | any = '';
    let csrfToken: string | any;

    onMount(async () => {
        csrfToken = getCookie('csrftoken');
    });
  
    async function register() {
      try {
        const response = await fetch('/api/register', { // Adjust the URL as needed
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 
                username: username, 
                first_name: firstName, 
                last_name: lastName, 
                email: email, 
                password: password, 
                password2: confirmPassword, 
                user_wallet_address: userWalletAddress 
            })
        });
  
        const data = await response.json();

        if (response.ok) {
            // TODO: Show success toast with data.message
            console.log('Registration successful:', data);
            navigate('/', { replace: true }); // Navigate to the index page
        } else {
            errorMessage = data.message;
            console.log('Registration errors:', data)
            console.log('Registration errorMessage:', errorMessage)
            throw new Error(errorMessage);

        }
      } catch (error) {
            console.error('Registering unsuccessful in catch:', error);
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
  
  <form on:submit|preventDefault={register}>
    <input type="text" placeholder="Username" bind:value={username} required />
    <input type="text" placeholder="First Name" bind:value={firstName} required />
    <input type="text" placeholder="Last Name" bind:value={lastName} required />
    <input type="email" placeholder="Email" bind:value={email} required />
    <input type="password" placeholder="Password" bind:value={password} required />
    <input type="password" placeholder="Confirm Password" bind:value={confirmPassword} required />
    <input type="text" placeholder="Wallet Address" bind:value={userWalletAddress} />
    <button type="submit">Register</button>
  </form>
  