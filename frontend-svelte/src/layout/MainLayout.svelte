<script lang="ts">
    
    // local state variables - to be changed as per needs. Will be passed on to child components if needed
    export let isSignedIn: boolean;

</script>

<div class="grid-container">
    <div class="grid-header">
        <slot name="header-content"/>
    </div>

    <div class="grid-navbar">
        <slot name="header-navbar" />
    </div>

    <main class={isSignedIn ? "grid-main with-sidebar" : "grid-main no-sidebar"}>

        <slot name="content" />
        
    </main>

    <div class="grid-footer">
        <slot name="footer" />
    </div>
</div>

<style>
    .grid-header {
        grid-area: gr-header;
    }
    
    .grid-navbar {
        grid-area: gr-navbar;
    }
    
    .grid-main {
        grid-area: gr-main;
    }
    
    .grid-footer {
        grid-area: gr-footer;
    }

    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto 1fr auto;
        grid-template-areas:
            "gr-header gr-navbar"
            "gr-main gr-main"
            "gr-footer gr-footer";
        min-height: 100vh;
    }
    
</style>
