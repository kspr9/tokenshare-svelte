<script lang="ts">

    export let workspace: any;
    export let company: any;

</script>

<div class="card">
    <div class="card-header">
      {workspace.workspace_name}
    </div>
    <div class="card-body">
      <p>{workspace.workspace_description}</p>
      <p><strong>Company:</strong> {company.name}</p>
      <p><strong>Registration Number:</strong> {company.reg_number}</p>
      <p><strong>Max Shares:</strong> {company.max_number_of_shares}</p>
    </div>
    <div class="card-footer">
      Members: {workspace.workspace_members.length}
    </div>
</div>

<style>
    /* Add your CSS styling here */
</style>