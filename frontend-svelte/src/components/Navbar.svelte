<script lang="ts">

  // props declarations
  export let isSignedIn:boolean;
</script>

<nav>
  <!-- Shared navigation items -->
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/open-funding-calls">Open Funding Calls</a>
  {#if isSignedIn}
    <!-- Items shown when the user is signed in -->
    <a href="/logout">Log Out</a>
  {:else}
    <!-- Items shown when the user is not signed in -->
    <a href="/signin">Sign In</a>
    <a href="/signup">Register</a>
  {/if}
</nav>