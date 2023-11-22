## TODO Separate views into individual files, such as auth_user_views, governance_views etc

'''
    views for:
        Dashboard
            get
        workspaces
            get
        workspace<int:workspace_id> ie workspace detail view
            get (get a workspace + associated gov contract and contract assets (ie companies))
            post (create a new workspace, specify company, deploy contract etc)
        settings
            get
            update
        profile
            get
            update
        company
            get
            post
            update
        contract
            get
            post
            update
'''