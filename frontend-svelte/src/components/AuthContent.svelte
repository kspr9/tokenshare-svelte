<script lang="ts">
    console.log("AuthContent component is being initialized");
    import Counter from "../lib/Counter.svelte";
    import Sidebar from "./Sidebar.svelte";

    import { onMount } from "svelte";

    export let username: string;
    console.log("Username:", username);
    
    let apimessage = "waiting for server...";

    onMount(async () => {
        let res = await fetch("/api/greet").then((res) => res.json());
        console.log(res);
        apimessage = JSON.stringify(res);
    });
</script>

<div class="sidebar-div">
    <Sidebar />
</div>
<div class="content-container">
    <!-- signed-in user content -->
    <h3>Welcome to your dashboard.</h3>
    To manage your companies or create one, navigate to your Workspaces
    <br>
    <div class="card">
        <Counter />
    </div>
    <h4>Hello {username}!</h4>

    <h3>Data from server</h3>
    {apimessage}
</div>

<style>
    
    
    
    .sidebar-div {
        background-color: #333;
    }

    .sidebar-div,
    .content-container {
        display: flex;
        flex-direction: column;
    }
    .content-container {
        flex: 1;
    }  


</style>
