from flask import current_app
from flask_principal import identity_changed, Identity, identity_loaded, Permission, RoleNeed, UserNeed
from flask_login import current_user

admin_permission = Permission(RoleNeed('admin'))

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    
    # Set the identity user object
    identity.user = current_user
    
    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Update the identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles.split(','):
            identity.provides.add(RoleNeed(role))
