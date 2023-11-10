<script lang="ts">
    import Header from "../components/Header.svelte";
    import Navbar from "../components/Navbar.svelte";
    import Footer from "../components/Footer.svelte";
    import Content from "../components/Content.svelte";
    import AuthContent from "../components/AuthContent.svelte";

    // local state variables - to be changed as per needs. Will be passed on to child components if needed
    let isSignedIn = false;

    let name: string = "Kaspar";
</script>

<div class="grid-container">
    <div class="grid-header">
        <Header />
    </div>

    <div class="grid-navbar">
        <Navbar {isSignedIn} />
    </div>
    
    <main class="grid-main">
        {#if isSignedIn}
            <div class="main-section with-sidebar">
                <AuthContent {name} />
            </div>
        {:else}
            <div class="main-section no-sidebar">
                <Content />
            </div>
        {/if}
    </main>

    <div class="grid-footer">
        <Footer />
    </div>
</div>

<style>
    .grid-container {
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr auto;
        grid-template-areas:
            "header"
            "navbar"
            "content"
            "footer";
        min-height: 100vh;
    }

    .grid-header {
        grid-area: header;
    }

    .grid-navbar {
        grid-area: navbar;
    }

    .grid-main {
        grid-area: content;
    }

    .grid-footer {
        grid-area: footer;
    }
</style>
