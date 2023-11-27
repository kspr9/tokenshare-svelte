<script>

    

    export let read = false;

</script>

<div class={read ? "email-element read" : "email-element unread text-muted"}>
    <div class="msg-content">
        
        <slot name="pre_description"/>
        {#if $$slots.sender}
            <slot name="sender"/>
        {/if}
        {#if $$slots.recipients}
            <slot name="recipients"/>
        {/if}
    
        <slot name="subject"/>
    
        <slot name="timestamp" class="date"/>
        
    </div>
</div>

<style>
    .email-element {
        border: solid 3px;
        margin: 10px;
    }
    .read {
        background-color: "grey";
        color: black;
    }
    .unread {
        background-color: "white";
    }
    .msg-content {
        padding: 10px;
    }
    .date {
        float: right;
        
    }
</style>