<script lang="ts">

    import { Router, Route } from "svelte-routing";
    import { onMount } from "svelte";

    // Component imports
    ////////////////////
    import Header from "./components/Header.svelte";
    //import Navbar from "./components/Navbar.svelte";
    import Sidebar from "./components/Sidebar.svelte";
    import Profile from "./content/Profile.svelte";
    import Workspaces from "./content/Workspaces.svelte";
    import Messages from "./content/Messages.svelte";
    import Settings from "./content/Settings.svelte";
    import NoSignInIndex from "./content/NoSignInIndex.svelte";
    //import AuthContent from "./components/AuthContent.svelte";
    //import MainLayout from "./layout/MainLayout.svelte";
    import Footer from "./components/Footer.svelte";

    // type imports
    import type { UserProps } from './types/userProps';

    let isSignedIn: boolean = false;
    let apimessage = "waiting for server...";
    
    let userProps: UserProps;

    onMount(async () => {
        let res = await fetch("/api/auth-user").then((res) => res.json());
        console.log(res);
        apimessage = JSON.stringify(res);
        userProps = {
            pk: res.userData.pk,
            username: res.userData.username,
            email: res.userData.email,
            first_name: res.userData.first_name,
            last_name: res.userData.last_name
        };
        isSignedIn = res.isSignedIn;
        console.log(isSignedIn, userProps.username);
    });
    // console.log(isSignedIn, userProps.username);
    

</script>

<Header {isSignedIn}/>

<Router>
    <main class={isSignedIn ? "grid-main with-sidebar" : "grid-main no-sidebar"}>

        {#if isSignedIn}
            <Sidebar />
            <Route path="">
                <Workspaces {userProps} />
            </Route>
            <Route path="/messages" component={Messages} />
            <Route path="/profile" component={Profile} />
            <Route path="/settings" component={Settings} />
        {:else}
            <Route path="" component={NoSignInIndex} {isSignedIn}/>
        {/if}
    
    </main>
</Router>

<Footer />


<style>
    main {
        display: flex;
        flex-direction: row;
    }
</style>
