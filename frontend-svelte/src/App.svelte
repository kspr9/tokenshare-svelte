<script lang="ts">
  
  import Counter from './lib/Counter.svelte';

  import { onMount } from "svelte";

  export let name: string;

  let apimessage = "waiting for server...";

  onMount(async () => {
    let res = await fetch("/api/greet")
    .then((res) => res.json());
    console.log(res);
    apimessage = JSON.stringify(res);
  });

</script>

<main>
    <div class="card">
      <Counter />
    </div>  
    <h1>Hello {name}!</h1>

    <h3>Data from server</h3>
    {apimessage}
</main>

<style>
  
</style>
