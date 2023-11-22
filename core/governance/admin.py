from django.contrib import admin


from .models import Company, CompanyShares, CompanyRoles, AuditTrail, TimelineEvent

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyShares)
admin.site.register(CompanyRoles)
admin.site.register(AuditTrail)
admin.site.register(TimelineEvent)