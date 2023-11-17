<script lang="ts">
    console.log("AuthContent component is being initialized");
    import { onMount } from "svelte";
    
    import Counter from "../lib/Counter.svelte";

    import type { UserProps } from '../types/userProps';

    export let userProps: UserProps;

    console.log("Username:", userProps.username);
    
    let apimessage = "waiting for server...";

    onMount(async () => {
        let res = await fetch("/api/greet").then((res) => res.json());
        console.log(res);
        apimessage = JSON.stringify(res);
    });
</script>


<div class="content-container">
    <!-- signed-in user content -->
    <h4>Hello {userProps.username}!</h4>
    <h3>Welcome to your dashboard.</h3>
    To manage your companies or create one, navigate to your Workspaces
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