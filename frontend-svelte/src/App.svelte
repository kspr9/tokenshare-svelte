<script lang="ts">
    
    import Header from "./components/Header.svelte";
    import Navbar from "./components/Navbar.svelte";
    import Content from "./components/Content.svelte";
    import AuthContent from "./components/AuthContent.svelte";
    import MainLayout from "./layout/MainLayout.svelte";
    import Footer from "./components/Footer.svelte";

    import { onMount } from "svelte";

    let isSignedIn: boolean = false;
    let username: string = "";
    let apimessage = "waiting for server...";

    onMount(async () => {
        let res = await fetch("/api/auth-user").then((res) => res.json());
        console.log(res);
        apimessage = JSON.stringify(res);
        isSignedIn = res.isSignedIn;
        username = res.userData ? res.userData.username : null;
        console.log(isSignedIn, username);
    });
    console.log(isSignedIn, username);
    

</script>

<MainLayout {isSignedIn}>
    <Header slot="header-content"/>
    <Navbar slot="header-navbar" {isSignedIn} />
    
    {#if isSignedIn}
        <AuthContent slot="content" {username} />        
    {:else}
        <Content slot="content" {isSignedIn}/>
    {/if}

    <Footer slot="footer" />

</MainLayout>

<style>
</style>
