from django.db import models

from django.core.exceptions import ValidationError

# for adding values to AuditTrail using signals
from django.db.models.signals import post_save
from django.dispatch import receiver


from core.accounts.models import User








# Base class for governing shares of a company
class GovernanceContract(models.Model):
    CONTRACT_CHOICES = (
        ('Business', 'Business'),
        ('Personal', 'Personal'),
    )
    governance_type = models.CharField(max_length=255, choices=CONTRACT_CHOICES)

    #contract_id = models.AutoField(primary_key=True)

    # Contract address is added after the contract has been deployed
    contract_address = models.CharField(max_length=255, blank=True)

    # the tezos address of a User who creates the workspace
    # from governed_company.admin_user.user_wallet_address
    admin_address = models.CharField(max_length=255)

    '''
    attributes via other models:
        'owned_company_shares' from CompanyShares model
        'governed_company' from Company model
        'governed_personal_company' from PersonalCompany model
        'ws_governance_contract' from Workspace model
    '''

    def clean(self):
        # Check if both relations exist
        if hasattr(self, 'governed_company') and hasattr(self, 'governed_personal_company'):
            raise ValidationError("A GovernanceContract can't be related to both a Company and a PersonalCompany.")
        
        super().clean()  # call the parent's clean method.

    def save(self, *args, **kwargs):
        self.full_clean()  # run the clean method and validate the model instance.
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.contract_address=} adminned by {self.admin_address}'


'''
class ProxyCompanyModel(models.Model):
    # Governance Contract will be created after a company is created
    # maybe handled by signals?
    # maybe via view logic
    # Once the associated Contract object is created, it will be assigned to this model

    
    # TODO: later, the admin user can be checked by the governance contract admin address
    #       and user can be identified by which user commands the wallet address
    # meaning that admin_user should eventually == owner of the admin_address of the governance contract
    #admin_user = models.ForeignKey(User, 
    #                               related_name='admin_in_companies', 
    #                               on_delete=models.PROTECT)
    
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True
'''



# Company Model
class Company(models.Model):
    name = models.CharField(max_length=255)
    reg_number = models.PositiveIntegerField()
    max_number_of_shares = models.PositiveIntegerField()

    # Each Company instance can be represented/governed by one contract
    # does not represent 'owner' of a Company, rather 'a manager' or a 'governance space'
        # If a governor company wants to 'own' shares, it is done
        # by the governing contract owning CompanyShares
    governing_contract = models.OneToOneField(GovernanceContract, 
                                         related_name='governed_company', 
                                         on_delete=models.PROTECT, 
                                         blank=True, null=True
                                         )

    ''' attributes via other models:
        'asset_in_workspace' -from Workspace model
            A company becomes an asset in a workspace, if
            the governor contract of the WS owns shares in a company
    '''
    
    '''
    shares_held_in_other_companies = models.ManyToManyField('self', 
                                                           through='CompanyShares', 
                                                           through_fields=('owner_contract', 'company'),
                                                           related_name='corporate_shareholder',
                                                           symmetrical=False, 
                                                           blank=True)
    
    
    # This property fetches all CompanyShares where the governing contract is this Company's governance contract
    @property
    def shares_owned(self):
        return CompanyShares.objects.filter(governing_contract=self.governance_contract)
    '''
    # custom behaviour for when a company is deleted
    # NOTE! If the model instances are deleted in bulk using the QuerySet’s delete method, 
    # the custom delete method will not be called.
    def delete(self, *args, **kwargs):
        audit_objects = AuditTrail.objects.filter(company=self)
        for audit_object in audit_objects:
            audit_object.company = None
            audit_object.metadata += {'deleted_company_contract_address': self.governance_contract.contract_address}
            audit_object.save()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name=} ({self.reg_number=})'


# Abstraction model for handling governance, shares ownership 
# and workspaces for Users the same way as for Companies
# The users relation to a company is through the wallet_address that is tied to a Governance contract
# the governance contract, in turn, has the relation to a Company model
class PersonalCompany(models.Model):
    name = models.CharField(max_length=255)
    governing_contract = models.OneToOneField(GovernanceContract, 
                                         related_name='governed_personal_company', 
                                         on_delete=models.PROTECT, 
                                         blank=True, null=True
                                        )


# Share Model (Intermediary for ManyToMany)
class CompanyShares(models.Model):
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
    
    ## Should CompanyShares have, instead of 'holder', a governing contract?
    ## the idea is that the app should not care about to which user the shares belong to
    ## it only cares about which contract governs the shares.
    ## if you have access to the contract, then you are the one who owns, 
    # and thus can govern

    # NOTE: for the purpose of keeping data synced, the transfer of shares should be
    #   --> performed through the portal involving a signature of the portal's main contract
    #   this way we can ensure the changes are reflected in the portal DB as well, and 
    #   transfers cannot happen merely by executing transactions on the blockchain
    ''' Represents the Owner of a Share '''
    governing_contract = models.ForeignKey(GovernanceContract, 
                                           related_name='owned_company_shares',
                                           on_delete=models.PROTECT, 
                                           blank=True, null=True
                                          )

    date_last_ownership_change = models.DateField(blank=True)
    vesting_start_date = models.DateField(blank=True)
    vesting_period = models.DurationField(blank=True)

    
    @property
    def holder(self):
        return self.governing_contract.contract_address
    
    def __str__(self):
        return f"{self.holder} ({self.governing_contract.governance_type}) owns {self.shares_amount} {self.get_share_type_display()} shares in {self.company.company_name}"

    


# Workspace Model
class Workspace(models.Model):
    #workspace_id = models.AutoField(primary_key=True)
    workspace_name = models.CharField(max_length=255)
    workspace_description = models.TextField(blank=True)
    workspace_logo = models.ImageField(null=True, blank=True)
    workspace_owner = models.ForeignKey(User, 
                                        related_name='owned_workspace', 
                                        on_delete=models.PROTECT)
    
    # WS governor contract
    '''
        TODO: Does a ws governor contract require always that there is a Company instance?
        Could there be a business governance contact without a Company?
        I think not. you would create a Company, and that deploys the governance contract

        Was wondering about if governor needs to be a Contract or a Company.
        seems like it cannot be a company, it creates complexity since 
        governor could be either User or Company, and governor attribute should accommodate both
        So to make it simpler, ws_governor should be a GovernanceContract, 
        and then it does not matter which is the manager of the governance contract
    '''
    ws_governor_contract = models.OneToOneField(GovernanceContract, 
                                         related_name='governed_workspace', 
                                         blank=True, null=True, 
                                         on_delete=models.PROTECT)
    
    # TODO: This might be redundant, as assets can be loaded via 
    #   the ws_governor_contract.owned_company_shares.issuing_company.get_unique etc
    #workspace_assets = models.ManyToManyField(Company, 
    #                                          related_name='asset_in_workspace', 
    #                                          blank=True)
    # might be redundant, since permission to perform actions in 
    # the governor company of the workspace, would be managed by CompanyRoles
    workspace_members = models.ManyToManyField(User, 
                                               related_name='member_in_workspaces', 
                                               blank=True)


    def __str__(self):
        return f"Workspace {self.workspace_name} is governed by contract: {self.ws_governor_contract.contract_address}"
    
        
# Role Model - giving role based privileges or responsibility in a company
class CompanyRoles(models.Model):
    
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
        return f"{self.user.username} has a {self.get_role_type_display()} role in {self.company.name}"

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
            updates['users_wallet'] = instance.user.wallet_address

        if instance.company:
            updates['company_contract'] = instance.company.company_contract_address

        if updates:
            AuditTrail.objects.filter(pk=instance.pk).update(**updates)