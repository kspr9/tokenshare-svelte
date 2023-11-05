<script lang="ts">
    
    import Header from "./layout/Header.svelte";
    import Navbar from "./layout/Navbar.svelte";
    import Footer from "./layout/Footer.svelte";
    import Content from "./layout/Content.svelte";
    import AuthContent from "./layout/AuthContent.svelte";

    // local state variables - to be changed as per needs. Will be passed on to child components if needed
    let isSignedIn = false;

    let name: string = "Kaspar";

    
</script>

<main>
    <Header />

    <Navbar {isSignedIn} />

    {#if isSignedIn}
        <div class="main-section">
            <AuthContent {name}/>
        </div>
    {:else}
        <div class="main-section">
            <Content />
        </div>
    {/if}

    <Footer />

</main>

<style>
</style>
