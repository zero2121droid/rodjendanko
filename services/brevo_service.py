import os
import brevo_python
from brevo_python.rest import ApiException

def _get_api_instance():
    """Lazy initialization of Brevo API instance"""
    api_key = os.getenv('BREVO_API_KEY')
    if not api_key:
        raise ValueError("BREVO_API_KEY environment variable is not set")
    
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = api_key
    return brevo_python.ContactsApi(brevo_python.ApiClient(configuration))

def add_contact_to_brevo(email, first_name="", last_name=""):
    api_instance = _get_api_instance()  # Get API instance when function is called
    
    create_contact = brevo_python.CreateContact(
        email=email,
        attributes={
            "FIRSTNAME": first_name,
            "LASTNAME": last_name,
        },
        list_ids=[5],  
        update_enabled=True
    )
    try:
        api_response = api_instance.create_contact(create_contact)
        print("Brevo response:", api_response)
        return api_response
    except ApiException as e:
        print("Exception when calling Brevo API: %s\n" % e)
        return None
