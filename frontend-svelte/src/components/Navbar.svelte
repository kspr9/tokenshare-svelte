<script lang="ts">
    import { Router, Link, Route } from "svelte-routing";
    import { isAuthenticated } from '../stores/userSession';
    
    let logoutUrl = `${window.location.origin}/accounts/logout`;
    

</script>

<nav>
  <!-- Shared navigation items -->
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/open-funding-calls">Open Funding Calls</a>
  {#if $isAuthenticated}
    <!-- Items shown when the user is signed in -->
    <a href={logoutUrl}>Log Out</a>
  {:else}
    <!-- Items shown when the user is not signed in -->
    <a href="/accounts/login">Sign In</a>
    <a href="/signup">Register</a>
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