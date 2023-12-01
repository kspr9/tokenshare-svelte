from django.db import models

from django.contrib.auth.models import AbstractUser



'''
# Abstract Model
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
'''
class NullableUniqueCharField(models.CharField):
    def get_prep_value(self, value):
        return value if value != '' else None

# Custom User Model
class User(AbstractUser):
    """User model - inherited from Django implementation"""
    """
    # Model fields:
        username
        first_name
        last_name
        email
        is_staff
        is_active
        date_joined
    """
    #user_id = models.AutoField(primary_key=True)
    user_wallet_address = NullableUniqueCharField(max_length=255, unique=True, null=True, blank=True)
    ''' To get all shares owned by the User
        we can get GovernanceContracts that the User wallet admins
        ie self.user_wallet_address == GovernanceContract.admin_address
            contracts = GovernanceContract.objects.filter(admin_address=self.user_wallet_address)
        and get all the shares 'owned_company_shares' from that contract
        OR through the self.admin_in_companies, Company.governance_contract,
        assuming admin_user.user_wallet_address in the Company always == contract.admin_address
    '''
    roles_in_companies = models.ManyToManyField('governance.Company', through='governance.CompanyRoles', related_name='users_with_roles', blank=True)

    '''
    attributes via other models:
        # deleted - 'admin_in_companies' from Company model  # i think I substituted this with WS owner
            Company model has governance_contract
            GovernanceContract has 'owned_company_shares' through CompanyShares model
        'owned_workspace' from Workspace model
        'member_in_workspaces' from Workspace model
    '''

    # storing the users wallet in the existing audit trails, but allowing to delete the user
    def delete(self, *args, **kwargs):
        from governance.models import AuditTrail
        audit_objects = AuditTrail.objects.filter(user=self)
        for audit_object in audit_objects:
            audit_object.user = None
            audit_object.metadata += {'deleted_user_wallet_address': self.user_wallet_address}
            audit_object.save()
        super().delete(*args, **kwargs)
