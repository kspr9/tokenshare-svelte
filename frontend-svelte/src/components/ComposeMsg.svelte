<script lang="ts">

    import { userData } from "../stores/userDataStore";

    export let onMessageSent: (view: string) => void;

    let recipients = '';
    let subject = '';
    let body = '';
    let username = $userData?.username;


    // SendEmail
    async function sendMessage() {
        const sending = await fetch('/user_comms/send_msg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log({result});
        })
        .then(() => {
            onMessageSent('sent');
        })
        .catch(error => {
            console.error('Error:', error);
        });

    }
</script>

<h2>Compose your message</h2>

<div id="compose-view">
    <h3>New Message</h3>
    <form id="compose-form" on:submit|preventDefault={sendMessage}>
        <div class="form-group">
            From: <input disabled class="form-control" bind:value={username}>
        </div>
        <div class="form-group">
            To: <input bind:value={recipients} class="form-control" placeholder="Recipients">
        </div>
        <div class="form-group">
            <input bind:value={subject} class="form-control" placeholder="Subject">
        </div>
        <textarea bind:value={body} class="form-control" placeholder="Your Message Here"></textarea>
        <input type="submit" class="btn btn-primary" value="Send" id="send-email" disabled={!$userData || !$userData.username}/>
    </form>
</div>