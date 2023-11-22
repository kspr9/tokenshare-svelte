from django.db import models

from django.contrib.auth.models import AbstractUser




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
    user_id = models.AutoField(primary_key=True)
    user_wallet_address = models.CharField(max_length=255, unique=True, null=True, blank=True)
    user_contract = models.ForeignKey('governance.GovernanceContract', 
                                         related_name='contract_owner', 
                                         on_delete=models.PROTECT, 
                                         blank=True, null=True
                                         )

    shares_owned_in_companies = models.ManyToManyField('governance.Company', 
                                    through='governance.CompanyShares', 
                                    through_fields=('user_holder', 'company'),
                                    related_name='shareholders', 
                                    blank=True)
    
    roles_in_companies = models.ManyToManyField('governance.Company', through='governance.CompanyRoles', related_name='users_with_roles', blank=True)


    # storing the users wallet in the existing audit trails, but allowing to delete the user
    def delete(self, *args, **kwargs):
        from governance.models import AuditTrail
        audit_objects = AuditTrail.objects.filter(user=self)
        for audit_object in audit_objects:
            audit_object.user = None
            audit_object.metadata += {'deleted_user_wallet_address': self.wallet_address}
            audit_object.save()
        super().delete(*args, **kwargs)