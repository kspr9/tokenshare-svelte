<script lang="ts">
    import Navbar from "./Navbar.svelte";
</script>

<style>
    .title {
        background-color: #333;
        color: white;
        padding: 0rem;
        font-size: 1em;
        text-align: left;
        width: 100%;
        margin-top: 1.25em;
    }

    .logo {
        background-color: green;
        height: 25%;
    }
    header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        /* Additional styling */
    }
</style>

<header>
    <div class="logo"></div>
    <div class="title">TokenShare Portal</div>
    <Navbar />
</header>