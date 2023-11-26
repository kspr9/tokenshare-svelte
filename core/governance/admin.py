from django.contrib import admin


from .models import (GovernanceContract, 
                     PersonalCompany, 
                     Company,
                     Workspace,
                     CompanyShares, 
                     CompanyRoles, 
                     AuditTrail, 
                     TimelineEvent
                     )

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyShares)
admin.site.register(CompanyRoles)
admin.site.register(AuditTrail)
admin.site.register(TimelineEvent)
admin.site.register(GovernanceContract)
admin.site.register(PersonalCompany)
admin.site.register(Workspace)