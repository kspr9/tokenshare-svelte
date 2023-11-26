<script lang="ts">

    // SendEmail
    async function send_email(event) {

        // Modifies the default beheavor so it doesn't reload the page after submitting.
        event.preventDefault();

        // define the variables taken from compose form field IDs
        const recipients = document.querySelector("#compose-recipients").value;
        const subject = document.querySelector("#compose-subject").value;
        const body = document.querySelector("#compose-body").value;

        const sending = await fetch('/mail/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
                
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log({result});
        });

        const unreading = await fetch("/mail/emails/sent")
            .then((response) => response.json()) // response is the data received from fetch
            .then((emails) => {
                console.log({emails});

                const email_id = Math.max(...emails.map(item => item.id));
                console.log({email_id});
                changeToUnread(email_id);
        });

        loadMailbox("sent");

    }
</script>

<h2>Compose your message</h2>

<form on:submit|preventDefault={sendMessage}>
    <input id="compose-recipients" bind:value={recipients} class="form-control" placeholder="Recipients">
    <input id="compose-subject" bind:value={subject} class="form-control" placeholder="Subject">
    <textarea id="compose-body" bind:value={body} class="form-control" placeholder="Message"></textarea>
    <button type="submit">Send Message</button>
</form>