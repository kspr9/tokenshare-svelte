from django.db import models

from django.core.exceptions import ValidationError

# for adding values to AuditTrail using signals
from django.db.models.signals import post_save
from django.dispatch import receiver


from core.accounts.models import User





# Company Model
class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"

    COMPANY_TYPES = (
        ('Business', 'Business'),
        ('Personal', 'Personal'),
    )
    company_type = models.CharField(max_length=255, choices=COMPANY_TYPES)
    name = models.CharField(max_length=255)
    
    # Admin of the company
    # from governing_contract.admin_address == user.user_wallet_address
    #admin_user = models.ForeignKey(User, related_name='admin_in_companies', on_delete=models.PROTECT)

    # Each Company instance can be represented/governed by one contract
    # does not represent 'owner' of a Company, rather 'a manager' or a 'governance space'
        # If a company wants to 'own' shares in other companies, it is done
        # by the governing contract owning CompanyShares issued by the other company
    

    # Conditionally applicable for 'Business' types only
    reg_number = models.PositiveIntegerField(blank=True, null=True)
    max_number_of_shares = models.PositiveIntegerField(blank=True, null=True)

    
    '''
    attributes via other models:
        company_workspace
        governing_contract
        shares_issued
        company_roles
    '''
    
    # This property fetches all CompanyShares where the governing contract is this Company's governance contract
    @property
    def shares_owned(self):
        return CompanyShare.objects.filter(governing_contract=self.governing_contract)

    # custom behaviour for when a company is deleted
    # NOTE! If the model instances are deleted in bulk using the QuerySet’s delete method, 
    # the custom delete method will not be called.
    def delete(self, *args, **kwargs):
        audit_objects = AuditTrail.objects.filter(company=self)
        for audit_object in audit_objects:
            audit_object.company = None
            audit_object.metadata += {'deleted_company_contract_address': self.governing_contract.contract_address}
            audit_object.save()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name=} ({self.reg_number=})'



# Base class for governing shares of a company
class GovernanceContract(models.Model):
    CONTRACT_CHOICES = (
        ('Business', 'Business'),
        ('Personal', 'Personal'),
    )
    governance_type = models.CharField(max_length=255, choices=CONTRACT_CHOICES)

    # Contract address is added after the contract has been deployed
    contract_address = models.CharField(max_length=255, blank=True)

    # the tezos address of a User who creates the Company
    admin_address = models.CharField(max_length=255)

    # governed company
    governed_company = models.OneToOneField(Company, 
                                            related_name='governing_contract', 
                                            on_delete=models.PROTECT, 
                                            blank=True, null=True
                                            )

    '''
    attributes via other models:
        owned_company_shares
    '''
    
    def __str__(self):
        return f'{self.contract_address=} adminned by {self.admin_address}'


# Share Model (Intermediary for ManyToMany)
class CompanyShare(models.Model):
    SHARE_CHOICES = (
		('A', 'class A'),
		('B', 'class B'),
		('C', 'class C'),
    )
    # which company issued these shares
    issuing_company = models.ForeignKey(Company, 
                                related_name='shares_issued', 
                                on_delete=models.PROTECT)
    
    # amount of shares that are combined into one Shares instance
    shares_amount = models.PositiveIntegerField()
    share_type = models.CharField(max_length=10, choices=SHARE_CHOICES)
    date_issued = models.DateTimeField(auto_now_add=True)
    

    # NOTE: for the purpose of keeping data synced, the transfer of shares should be
    #   --> performed through the portal involving a signature of the portal's main contract
    #   this way we can ensure the changes are reflected in the portal DB as well, and 
    #   transfers cannot happen merely by executing transactions on the blockchain
    
    ''' Represents the Owner of a Share '''
    owning_contract = models.ForeignKey(GovernanceContract, 
                                           related_name='owned_company_shares',
                                           on_delete=models.PROTECT, 
                                           blank=True, null=True
                                          )

    date_last_ownership_change = models.DateField(blank=True)
    
    ## TODO: create a separate model for vesting and move these attributes there
    #vesting_start_date = models.DateField(blank=True)
    #vesting_period = models.DurationField(blank=True)

    
    @property
    def holder(self):
        return self.owning_contract.contract_address
    
    def __str__(self):
        return f"{self.shares_amount} {self.share_type} shares in {self.issuing_company.name} owned by {self.holder} ({self.owning_contract.governance_type})"

    


# Workspace Model
class Workspace(models.Model):
    #workspace_id = models.AutoField(primary_key=True)
    workspace_name = models.CharField(max_length=255)
    workspace_description = models.TextField(blank=True)
    workspace_logo = models.ImageField(null=True, blank=True)
    workspace_owner = models.ForeignKey(User, 
                                        related_name='owned_workspace', 
                                        on_delete=models.PROTECT)
    
    # WS governor company
    ws_governor_company = models.OneToOneField(Company, 
                                         related_name='company_workspace', 
                                         blank=True, null=True, 
                                         on_delete=models.PROTECT)
    
    
    workspace_members = models.ManyToManyField(User, 
                                               related_name='member_in_workspaces', 
                                               blank=True)


    def __str__(self):
        return f"Workspace {self.workspace_name} is governed by contract: {self.ws_governor_company.governing_contract.contract_address}"
    
        
# Role Model - giving role based privileges or responsibility in a company, or in a workspace
class CompanyRole(models.Model):
    
    ROLE_CHOICES = (
        ('CEO', 'CEO'),
        ('Secretary', 'Secretary'),
		('Guest', 'Guest'),
		('Shareholder', 'Shareholder'),
        ('Employee', 'Employee'),
        ('Basic', 'Basic'),
    )

    user = models.ForeignKey(User, related_name='roles_in_company', on_delete=models.CASCADE)
    company = models.ForeignKey(Company,related_name='company_roles', on_delete=models.CASCADE)
    role_type = models.CharField(max_length=50, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'company', 'role_type')
    
    def __str__(self):
        return f"{self.user.username} has a {self.role_type} role in {self.company.name}"

# Events model
class TimelineEvent(models.Model):
    EVENT_CHOICES = [
        ('Created', 'Created'),
        ('Updated', 'Updated'),
        ('Deleted', 'Deleted'),
        ('Issued', 'Issued'),
        ('Transferred', 'Transferred'),
        ('Minted', 'Minted'),
        ('Deployed', 'Deployed'),
        ('Revoked', 'Revoked'),
        ('Granted', 'Granted'),
        ('Assigned', 'Assigned'),
        ('Started', 'Started'),
        ('Ended', 'Ended'),
        ('Cancelled', 'Cancelled'),
        ('Claimed', 'Claimed'),
        ('Voted', 'Voted'),
        ('Counted', 'Counted'),
    ]
    event_id = models.AutoField(primary_key=True)
    event_type = models.CharField(max_length=40, choices=EVENT_CHOICES)
    event_content = models.JSONField()
    event_time = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)

    # References to other models
    company = models.ForeignKey(Company, related_name='company_events', on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, related_name='workspace_events', on_delete=models.CASCADE)


# AuditTrail Model
class AuditTrail(models.Model):
    audit_id = models.AutoField(primary_key=True)
    
    change_event = models.ForeignKey(TimelineEvent, on_delete=models.SET_NULL, null=True)
    change_time = models.DateTimeField(auto_now_add=True)
    change_content = models.JSONField()

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    users_wallet = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    company_contract = models.CharField(max_length=255, blank=True, null=True)

    metadata = models.JSONField(null=True, blank=True)



### Signals

# Trigger when an AuditTrail object is saved - stores the wallet addresses without direct reference to the referenced object
@receiver(post_save, sender=AuditTrail)
def set_wallets_in_trail(sender, instance, **kwargs):
        updates = {}
        if instance.user:
            updates['users_wallet'] = instance.user.user_wallet_address

        if instance.company:
            updates['company_contract'] = instance.company.governing_contract.contract_address

        if updates:
            AuditTrail.objects.filter(pk=instance.pk).update(**updates)