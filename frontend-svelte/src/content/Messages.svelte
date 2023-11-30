<script lang="ts">
    import { onMount } from 'svelte';
    import MsgInMailbox from '../components/MsgInMailbox.svelte';
    import ComposeMsg from '../components/ComposeMsg.svelte';

    import type { Email } from '../types/email';

    import { userData } from "../stores/userDataStore";
  
    //let emails: Email | any = [];

    let currentView: string = 'inbox';

    let recipients = '';
    let subject = '';
    let body = '';
    let username = $userData?.username;
  
    onMount(async () => {
        displayMessageHubView('inbox');
    });
  
    
    async function displayMessageHubView(view:string) {
        // render currentView in the component according to view
        currentView = view;
    }
    
    async function loadMailbox(selectedMailbox: string) {
      const response = await fetch(`/user_comms/message_hub/${selectedMailbox}`);
      const emails = await response.json();
      return emails;
    }

    

    function readEmail() {
            // TODO
    }

    // TODO make MsgInMailbox clickable toggling read/unread
    
</script>

<div class="mailbox-container">
    <h1>Messages</h1>

    <div class="msg-controls">
        <button id="inbox-btn" on:click={() => displayMessageHubView('inbox')}>Inbox</button>
        <button id="compose-btn" on:click={() => displayMessageHubView('compose')}>New Message</button>
        <button id="sent-btn" on:click={() => displayMessageHubView('sent')}>Sent</button>
        <button id="archived-btn" on:click={() => displayMessageHubView('archived')}>Archived</button>
    </div>


    {#if currentView === 'inbox'}
        <h2>Inbox</h2>
        {#await loadMailbox('inbox')}
            <p>Loading inbox data...</p>
        {:then emails} 
            {#each emails as email}
                <MsgInMailbox>
                    <span class="pre_description" slot="pre_description">
                        Received from:
                    </span>
                    <div class="sender" slot="sender">
                            {email.sender}
                    </div>
                    <div class="subject" slot="subject">
                        Subject: {email.subject}
                    </div>
                    <div class="date" slot="timestamp">
                        Date: {email.timestamp}
                    </div>
                </MsgInMailbox>          

            {/each}
        {:catch error}
            <p>Error loading inbox: {error.message}</p>
        {/await}
    {:else if currentView === 'sent'}
        <h2>Sent</h2>
        {#await loadMailbox('sent')}
            <p>Loading sentbox data...</p>
        {:then emails}
            {#each emails as email}
                <MsgInMailbox>
                    <span class="pre_description" slot="pre_description">
                        Sent to:
                    </span>
                    <div class="recipients" slot="recipients">
                        {#each email.recipients as recipient}
                            {recipient}
                        {/each}
                    </div>
                    <div class="subject" slot="subject">
                        Subject: {email.subject}
                    </div>
                    <div class="date" slot="timestamp">
                        Date: {email.timestamp}
                    </div>
                </MsgInMailbox>          
            {/each}
        {:catch error}
            <p>Error loading sentbox: {error.message}</p>
        {/await}
    {:else if currentView === 'compose'}
    <ComposeMsg onMessageSent={displayMessageHubView}/>
    {:else if currentView === 'archive'}
        <h2>Archive</h2>
    {/if}

</div>
