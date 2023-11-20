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

    // Type imports
    import type { UserProps } from './types/userProps';

    // Store imports
    import { isAuthenticated } from "./stores/userSession";
    

    let apimessage = "waiting for server...";
    
    let userProps: UserProps;
    
    console.log("This is before the onMount");
    console.log($isAuthenticated);
    console.log("--------------");
    onMount(async () => {
        console.log("This is before the checkAuthenticationAndUpdateStore function");
        console.log($isAuthenticated);
        console.log("awaiting check-auth during onMount");
        await checkAuthenticationAndUpdateStore();
        console.log("await check-auth completed during onMount");
        console.log("This is after the await checkAuthenticationAndUpdateStore function");
        console.log($isAuthenticated);
        if ($isAuthenticated) {
            console.log("This should run ONLY when the user is authenticated");
            await fetchAuthenticatedUser();
        }
    });

    // Function to check authentication and update store
    async function checkAuthenticationAndUpdateStore() {
        console.log("Fetching check-auth data");
        let res = await fetch('/api/check-auth/');
        let data = await res.json();
        console.log("got the check-auth data");
        if (data.is_authenticated) {
            isAuthenticated.set(data.is_authenticated);  // Update the store value
            console.log("User is authenticated and isAuthenticated state changed");
            console.log($isAuthenticated);
            console.log("Auth check performed successfully");
        } else {
            console.log("User is not authenticated");
            $isAuthenticated = false;  // Update the store value
            console.log("isAuthenticated state (using $store= syntax):");
            console.log($isAuthenticated);
        };
    }

    // Function to fetch authenticated user data
    async function fetchAuthenticatedUser() {
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
            console.log(userProps.username);
        } catch (error) {
            console.error('Unauthenticated user session:', error);
        }
    }

    //let promise = fetchAuthenticatedUser();
    
</script>

<Header />

<Router>
    <main class={$isAuthenticated ? "grid-main with-sidebar" : "grid-main no-sidebar"}>

        
        {#if $isAuthenticated}
            <Sidebar />
            <Route path="">
                <Workspaces {userProps} />
            </Route>
            <Route path="/messages" component={Messages} />
            <Route path="/profile" component={Profile} />
            <Route path="/settings" component={Settings} />
        {:else}
            <Route path="" component={NoSignInIndex} />
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
