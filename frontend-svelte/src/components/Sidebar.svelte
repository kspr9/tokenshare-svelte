<script>
    import { Link } from "svelte-routing";

</script>

<div class="sidebar-container">
    <div class="sidebar-top">
        <Link to="/app/dashboard">Dashboard</Link>
        <Link to="/app/workspaces">Workspaces</Link>
        <Link to="/app/messages">Messages</Link>
    </div>
    <div class="sidebar-bottom">
        <Link to="/app/profile">Profile</Link>
        <Link to="/app/settings">Settings</Link>
    </div>
</div>

<style>
    .sidebar-container {
        min-height: 100%;
        min-height: 100dvh;
        width: 15dvw;
    }

    .sidebar-top {
        display: flex;
        flex-direction: column;
    }

    .sidebar-bottom {
        display: flex;
        flex-direction: column;
    }


</style>