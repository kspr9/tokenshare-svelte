<script lang="ts">
    import Counter from "../lib/Counter.svelte";
    import Sidebar from "./Sidebar.svelte";

    import { onMount } from "svelte";

    export let name: string;

    let apimessage = "waiting for server...";

    onMount(async () => {
        let res = await fetch("/api/greet").then((res) => res.json());
        console.log(res);
        apimessage = JSON.stringify(res);
    });
</script>

<div class="auth-content">
    <div class="sidebar-div">
        <Sidebar />
    </div>
    <div class="content">
        <!-- signed-in user content -->
        <h3>Welcome to your dashboard.</h3>
        To manage your companies or create one, navigate to your Workspaces
        <br>
        <div class="card">
            <Counter />
        </div>
        <h4>Hello {name}!</h4>

        <h3>Data from server</h3>
        {apimessage}
    </div>
</div>

<style>
</style>
