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
    .card {
        border: 1px solid #ccc;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        margin-bottom: 20px;
        background-color: #333;
    }

    .card-header {
        background-color: #444;
        padding: 15px 20px;
        font-size: 1.2em;
        font-weight: bold;
        border-bottom: 1px solid #eee;
    }

    .card-body {
        padding: 20px;
        line-height: 1.5;
    }

    .card-body p {
        margin: 0 0 10px;
    }

    .card-footer {
        padding: 10px 20px;
        background-color: #444;
        text-align: right;
        border-top: 1px solid #eee;
    }

</style>