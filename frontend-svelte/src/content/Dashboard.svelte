<script lang="ts">
    console.log("Dashboard component is being initialized");
    import { onMount } from "svelte";
    import { userData } from "../stores/userDataStore";
    
    import Counter from "../lib/Counter.svelte";

    
    console.log("Username:", $userData);
    
    let apimessage = "waiting for server...";

    onMount(async () => {
        let res = await fetch("/api/greet").then((res) => res.json());
        console.log(res);
        apimessage = JSON.stringify(res);
    });
</script>


<div class="content-container">
    <!-- signed-in user content -->
    <h4>Hello {$userData?.username}!</h4>
    <h3>Welcome to your dashboard.</h3>
    To manage your companies or create one, navigate to your Workspaces
    <br>
    <br>
    <h2>Timeline Events below</h2>
    <p>Recent timeline events across all your workspaces</p>
    <br>
    <div class="card">
        <Counter />
    </div>

    <h3>Data from server</h3>
    {apimessage}
</div>

<style>
    
    
    .content-container {
        display: flex;
        flex-direction: column;
    }
    .content-container {
        flex: 1;
    }  


</style>