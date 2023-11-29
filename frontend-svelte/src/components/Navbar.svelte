<script lang="ts">
    import { Link } from "svelte-routing";
    import { isAuthenticated } from "../stores/isAuthenticatedStore";
    
    import { isLoginModalOpen } from "../stores/isLoginModalOpenStore";

    let logoutUrl = `${window.location.origin}/accounts/logout`;
    
    function openLoginModal() {
        console.log('open login modal');
        console.log($isLoginModalOpen);
        isLoginModalOpen.set(true);
        console.log($isLoginModalOpen);
    }

</script>

<nav>
  <!-- Shared navigation items -->
  <Link to="">Home</Link>
  <Link to="/about">About</Link>
  <Link to="/open-funding-calls">Open Funding Calls</Link>
  {#if $isAuthenticated}
    <!-- Items shown when the user is signed in -->
    <a href={logoutUrl}>Log Out</a>
  {:else}
    <!-- Items shown when the user is not signed in -->
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <span on:click={openLoginModal} class="link-style">Log In</span>
    <Link to="/signup">Register</Link>
  {/if}
</nav>

<style>
    nav {
        background-color: #333;
        color: white;
        font-size: 1em;
        text-align: right;
        width: 100%;
        margin-top: 1.25em;
    }
    
</style>