<script lang="ts">
    import { Link } from "svelte-routing";
    import { isAuthenticated } from "../stores/isAuthenticatedStore";
    let logoutUrl = `${window.location.origin}/accounts/logout`;
    

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
    <Link to="/login">Log In</Link>
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