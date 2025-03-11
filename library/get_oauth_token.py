#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

import json
import time
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account

def get_oauth_token(google_subject, google_private_key, scopes):
    # Create the credentials using the private key and subject
    credentials = service_account.Credentials.from_service_account_info(
        {
            "private_key": google_private_key,
            "client_email": google_subject,
        },
        scopes=scopes,
    )

    # Refresh the credentials to get the access token
    auth_request = Request()
    credentials.refresh(auth_request)
    
    return credentials.token

def main():
    # Define the arguments the module will accept
    module_args = dict(
        google_subject=dict(type='str', required=True),
        google_private_key=dict(type='str', required=True),
        scopes=dict(type='list', required=True),
    )

    # Create the module object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    try:
        # Get OAuth token
        token = get_oauth_token(
            module.params['google_subject'], 
            module.params['google_private_key'], 
            module.params['scopes']
        )
        
        # Return the result
        module.exit_json(changed=False, token=token)
    
    except Exception as e:
        # If an error occurs, report it back
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
