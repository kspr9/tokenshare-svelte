from core.accounts.models import User
from django.contrib.auth.models import AbstractUser




def print_model_fields(model, parent_model=None):
    
    child_fields = {field.name for field in model._meta.get_fields()}
    #print(f"Child Model: {model.__name__}")
    #print(f"Child Fields: {child_fields}")
    #print('-------------------------------------------------')

    parent_fields = set()
    if parent_model:
        parent_fields = {field.name for field in parent_model._meta.get_fields()}
    
    new_fields = child_fields - parent_fields
    #print('-------------------------------------------------')

    #print(f"New Fields: {new_fields}")
    
    #print('-------------------------------------------------')

    related_fields = {field.name for field in model._meta.get_fields() if field.is_relation}
    #print(f"Related Fields: {related_fields}")
    #print('-------------------------------------------------')
    direct_fields = new_fields - related_fields
    #print(f"Direct Fields: {direct_fields}")
    #print('-------------------------------------------------')

    print('-------------------------------------------------')
    if parent_model is not None:
        print(f'Default Django model {parent_model.__name__} Fields:')
        for field in parent_model._meta.get_fields():
            if hasattr(field, 'blank'):
                is_required = 'No' if field.blank else 'Yes'
            else:
                is_required = 'N/A'
            print(f"\t{field.name} (Type: {field.get_internal_type()}, Required: {is_required})")
    
    print('-------------------------------------------------')
    # Print fields directly declared on the model
    print(f"Direct model {model.__name__} Fields:")
    for field in model._meta.get_fields():
        if not field.is_relation and field.name not in parent_fields:
            if hasattr(field, 'blank'):
                is_required = 'No' if field.blank else 'Yes'
            else:
                is_required = 'N/A'
            print(f"\t{field.name} (Type: {field.get_internal_type()}, Required: {is_required})")


    # Print fields from related models
    print("\nRelated Fields:")
    for field in model._meta.get_fields():
        if field.is_relation and field.related_model.__name__ not in ['LogEntry', 'Group', 'Permission']:
            rel_type = field.get_internal_type()
            rel_model = field.related_model.__name__ if field.related_model else 'N/A'
            if hasattr(field, 'blank'):
                is_required = 'No' if field.blank else 'Yes'
            else:
                is_required = 'N/A'
            print(f"\t{field.name} (Type: {rel_type}, Related Model: {rel_model}, Required: {is_required})")

# Call the function for your User model
print_model_fields(User, AbstractUser)


'''

def print_model_fields(model):
    # Print fields directly declared on the model
    print("Direct Fields:")
    for field in model._meta.get_fields():
        if not field.is_relation:
        # This will print all fields, including those from related models
            print(field.name)

    # Print fields from related models
    print("\nRelated Fields:")
    for field in model._meta.get_fields():
        if field.is_relation:
            print(f"{field.name} (related field)")

# Call the function for your User model

print_model_fields(User)
'''