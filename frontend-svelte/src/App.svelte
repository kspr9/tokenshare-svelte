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
        try {
            let res = await fetch("/api/auth-user");
            if (!res.ok) {
                throw new Error("Network response was not ok");
            }
            let data = await res.json();
            console.log(data);
            apimessage = JSON.stringify(data);
            userProps = {
                pk: data.userData.pk,
                username: data.userData.username,
                email: data.userData.email,
                first_name: data.userData.first_name,
                last_name: data.userData.last_name
            };
            isSignedIn = data.isSignedIn;
            console.log(isSignedIn, userProps.username);
        } catch (error) {
            console.error('Unauthenticated user session:', error);
            isSignedIn = false;
        }
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
