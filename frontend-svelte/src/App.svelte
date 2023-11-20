<script lang="ts">

    import { Router, Route } from "svelte-routing";
    import { onMount } from "svelte";

    // Component imports
    ////////////////////
    import Header from "./components/Header.svelte";
    //import Navbar from "./components/Navbar.svelte";
    import Sidebar from "./components/Sidebar.svelte";
    import Profile from "./content/Profile.svelte";
    import Dashboard from "./content/Workspaces.svelte";
    import Workspaces from "./content/Dashboard.svelte";
    import Messages from "./content/Messages.svelte";
    import Settings from "./content/Settings.svelte";
    import NoSignInIndex from "./content/NoSignInIndex.svelte";
    //import AuthContent from "./components/AuthContent.svelte";
    //import MainLayout from "./layout/MainLayout.svelte";
    import Footer from "./components/Footer.svelte";
    import Login from "./content/Login.svelte";

    // Type imports
    import type { UserProps } from './types/userProps';

    // Store imports
    import { isAuthenticated } from "./stores/isAuthenticatedStore";
    import { userData } from "./stores/userDataStore";
    

    let apimessage = "waiting for server...";
    
    let userProps: UserProps;
    
    

    console.log("This is before the onMount");
    console.log($isAuthenticated);
    console.log("--------------");
    onMount(async () => {
        console.log("This is before the checkAuthentication function");
        console.log($isAuthenticated);
        console.log("Calling check-auth during onMount");
        
        const checkedAuthData = await checkAuthentication();
        $isAuthenticated = checkedAuthData.isAuthenticated;

        console.log("Await check-auth completed during onMount");
        console.log("This is isAuthenticated state after the await checkAuthentication function");
        console.log($isAuthenticated);

        if ($isAuthenticated) {
            console.log("This should run ONLY when the user is authenticated");
            const fetchedUserProps = await fetchUserProps();
            $userData = fetchedUserProps;
        }
    });

    // Function to check authentication
    async function checkAuthentication() {
        console.log("Fetching check-auth data");
        let res = await fetch('/api/check-auth/');
        let data = await res.json();
        console.log("Got the check-auth data from server");
        let isAuthenticated: boolean = data.is_authenticated;
        let authMessage:string = "";
        if (isAuthenticated) {
            authMessage += "User is authenticated. ";
            authMessage += "Auth check performed successfully. ";
        } else {
            authMessage += "User is not authenticated";
            authMessage += "Auth check performed successfully. ";
        };
        return {isAuthenticated, "message": authMessage};
    }

    // Function to fetch authenticated user data
    async function fetchUserProps() {
        try {
            let res = await fetch("/api/auth-user");
            if (!res.ok) {
                throw new Error("Network response was not ok");
            }
            let data = await res.json();
            console.log(data);

            const userProps = {
                pk: data.userData.pk,
                username: data.userData.username,
                email: data.userData.email,
                first_name: data.userData.first_name,
                last_name: data.userData.last_name
            };
            console.log(userProps.username);

            return userProps;
        } catch (error) {
            console.error('Unauthenticated user session:', error);
            throw error; // Re-throw the error to handle it in the calling context
        }
    }

    //let promise = fetchAuthenticatedUser();
    
</script>


<Router>
    <Header />
    <main class={$isAuthenticated ? "grid-main with-sidebar" : "grid-main no-sidebar"}>

        
        {#if $isAuthenticated}
            {#await fetchUserProps()}
                <!-- Loading state -->
                <p>Loading user data...</p>
            {:then}
                <!-- Success state -->
                <Sidebar />
                <Route path="" component={Dashboard} />
                <Route path="/app/workspaces">
                    <Workspaces />
                </Route>
                <Route path="/app/messages" component={Messages} />
                <Route path="/app/profile" component={Profile} />
                <Route path="/app/settings" component={Settings} />
            {:catch error}
                <!-- Error state -->
                <p>Error loading user data: {error.message}</p>
            {/await}
        {:else}
            <Route path="" component={NoSignInIndex} />
            <Route path="/login" component={Login} />
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
