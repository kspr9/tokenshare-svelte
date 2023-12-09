from django.contrib import admin


from .models import (GovernanceContract, 
                     Company,
                     Workspace,
                     CompanyShare, 
                     CompanyRole, 
                     AuditTrail, 
                     TimelineEvent
                     )

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyShare)
admin.site.register(CompanyRole)
admin.site.register(AuditTrail)
admin.site.register(TimelineEvent)
admin.site.register(GovernanceContract)
admin.site.register(Workspace)