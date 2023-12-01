<script lang="ts">

    import { Router, Route } from "svelte-routing";
    import { onMount } from "svelte";


    // Component imports
    ////////////////////
    import Header from "./components/Header.svelte";
    //import Navbar from "./components/Navbar.svelte";
    import Sidebar from "./components/Sidebar.svelte";
    import Profile from "./content/Profile.svelte";
    import Dashboard from "./content/Dashboard.svelte";
    import Workspaces from "./content/Workspaces.svelte";
    import Messages from "./content/Messages.svelte";
    import Settings from "./content/Settings.svelte";
    import NoSignInIndex from "./content/NoSignInIndex.svelte";
    //import AuthContent from "./components/AuthContent.svelte";
    //import MainLayout from "./layout/MainLayout.svelte";
    import Footer from "./components/Footer.svelte";
    import Login from "./content/Login.svelte";
    import Register from "./content/Register.svelte";

    // Type imports
    import type { UserProps } from './types/userProps';

    // Store imports
    import { isAuthenticated } from "./stores/isAuthenticatedStore";
    import { userData } from "./stores/userDataStore";
    import { isLoginModalOpen } from "./stores/isLoginModalOpenStore";
    

    let apimessage = "waiting for server...";
     
    

    console.log("This is before the onMount");
    console.log($isAuthenticated);
    console.log("--------------");
    onMount(async () => {
                        
        // since Login.svelte already updates $isAuthenticated, this check here is not needed
        //mockCheckAuthentication()
        checkAuthentication()
        .then(res => {
            isAuthenticated.set(res.isAuthenticated);
            console.log("inside onMount, after checkAuthentication .then");
            console.log($isAuthenticated);
        })
    
    });

    let userDataAvailable: boolean = false;
    
    isAuthenticated.subscribe(value => {
        if (value) {
            // TODO: change this function to fetchUserProps()
            // below function is intended for development
            //mockFetchUserProps()
            fetchUserProps()
            .then(userProps => {
                userData.set(userProps);
                userDataAvailable = true;
            })
            .then(() => {
                console.log("userData store updated");
                console.log($userData);
            })
            .catch(error => {
                console.error("Error fetching user data:", error);
                // Handle the error appropriately
            });
        }
    })
    

    // Function to check authentication
    async function checkAuthentication() {
        try {
            console.log("Fetching check-auth data");
            let res = await fetch('/api/check-auth/');

            // Check if the fetch request was successful
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            let data = await res.json();
            console.log("Got the check-auth data from server");

            let isAuthenticated = data.is_authenticated;
            let authMessage = "";

            if (isAuthenticated) {
                authMessage += "User is authenticated. ";
                authMessage += "Auth check performed successfully. ";
            } else {
                authMessage += "User is not authenticated. ";
                authMessage += "Auth check performed successfully. ";
            };

            return { isAuthenticated, "message": authMessage };
        } catch (error) {
            // Handle any errors that occurred during fetch or JSON parsing
            console.error("Error in authentication check:", error);
            return { isAuthenticated: false, message: "Failed to perform auth check due to an error." };
        }
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
            //userData.set(userProps);
            return userProps;
        } catch (error) {
            console.error('Unauthenticated user session:', error);
            throw error; // Re-throw the error to handle it in the calling context
        }
    }

    /*
    
    async function mockCheckAuthentication() {
        console.log("Fetching check-auth data");
            
        console.log("Got the check-auth data from server");

        let isAuthenticated = true;
        let authMessage = "";

        if (isAuthenticated) {
            authMessage += "User is authenticated. ";
            authMessage += "Auth check performed successfully. ";
        } else {
            authMessage += "User is not authenticated. ";
            authMessage += "Auth check performed successfully. ";
        };

        return { isAuthenticated, "message": authMessage };
    }

    // Function to fetch authenticated user data
    async function mockFetchUserProps() {
        const userProps = {
                pk: 1,
                username: 'kspr',
                email: 'kspr9@pm.me',
                first_name: 'Kaspar',
                last_name: 'Pae'
        };
        console.log(userProps.username);
        
        return userProps;
    }
    */


    
</script>


<Router>
    <Header />
    <main class={$isAuthenticated ? "grid-main with-sidebar" : "grid-main no-sidebar"}>

        
        {#if $isAuthenticated}
            {#await userDataAvailable}
                <!-- Loading state -->
                <p>Loading user data...</p>
            {:then}
                <!-- Success state -->
                <Sidebar />
                <Route path="" component={Dashboard} />
                <Route path="/app/dashboard" component={Dashboard} />
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
            {#if $isLoginModalOpen}
                <Login />
            {/if}
            <Route path="/signup" component={Register} />
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
