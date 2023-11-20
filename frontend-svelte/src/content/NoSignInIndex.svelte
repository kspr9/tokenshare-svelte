<script lang="ts">
    
    import { isAuthenticated } from "../stores/isAuthenticatedStore";
</script>

<div class="content-container-no-signin">
    <h2>Welcome to TokenShare portal</h2>
    <h3>You are signed in? {$isAuthenticated}</h3>
    <p>Tokenshare enables digitization of all governance operations of your company.</p>
    <p>
        This means, you can issue shares, transfer share ownership, hold shareholder meetings and vote on decisions.
        Any official documents (such as Articles of Association) can be independently validated through cryptographic hashing on the blockchain.
        <br>
        Voting results in legally binding decisions.

        Additionally, you can own shares of other companies through Tokenshare wallet contract. 
        Owning shares gives your voting rights as per the Articles of Association of each company
    </p>
    <p>Please Sign In or Register to continue.</p>
</div>