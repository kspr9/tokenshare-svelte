<script lang="ts">
    import { onMount } from 'svelte';
    import MsgInMailbox from '../components/MsgInMailbox.svelte';

    import type { Email } from '../types/email';
  
    let mailbox = 'inbox';
    let emails: Email | any = [];
  
    onMount(async () => {
      await loadMailbox(mailbox);
    });
  
    async function loadMailbox(selectedMailbox: string) {
      mailbox = selectedMailbox;
      const response = await fetch(`/mail/emails/${mailbox}`);
      emails = await response.json();
    }
    
    // TODO make MsgInMailbox clickable toggling read/unread
    
</script>

<h1>Messages</h1>

<button on:click={() => loadMailbox('inbox')}>Inbox</button>
<button on:click={() => loadMailbox('sent')}>Sent</button>


{#if mailbox === 'inbox'}
    <h2>Inbox</h2>
    {#each emails as email}
        <MsgInMailbox>
            <span class="pre_description" slot="pre_description">
                Received from:
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
{:else if mailbox=== 'sent'}
    <h2>Sent</h2>
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
{:else if mailbox === 'archive'}
    <h2>Archive</h2>
{/if}
