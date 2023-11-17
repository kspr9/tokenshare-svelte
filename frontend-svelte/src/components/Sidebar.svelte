<script>
    import { Link } from "svelte-routing";

</script>

<div class="sidebar-container">
    <div class="sidebar-top">
        <Link to="/workspaces">Workspaces</Link>
        <Link to="/messages">Messages</Link>
    </div>
    <div class="sidebar-bottom">
        <Link to="/profile">Profile</Link>
        <Link to="/settings">Settings</Link>
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