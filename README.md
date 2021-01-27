# MSALTest



## Azure App Registration:

Quickstart or manual. Important steps:

 * Add a reply URL as http://localhost:5000/getAToken (?)
 * Create a Client Secret (*)
 * Add Microsoft Graph API's User.ReadBasic.All delegated permission.

See

* https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/applicationsListBlade/quickStartType/PythonQuickstartPage/sourceType/docs


## Azure B2C User Flow

 * [Medium](https://medium.com/@sambowenhughes/what-is-an-azure-b2c-custom-policy-user-flow-7b8ed1c9baad)
 * [Docs](https://docs.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-user-flows)
 * [Docs2](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-v2-python-webapp)

## Flask

Client configuration:

 * client_id == secret key
 * client_credential == 
 * authority == Tenant ID
 
Authority value:

    "authority": "https://<tenantname>.b2clogin.com/<tenantname>.onmicrosoft.com"
 
### Server start

    cd <project-root-directory>
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ./run.sh
    
Should start the server at:

 * [localhost:5000](https://127.0.0.1:5000)
 
## See also

 * [Py examples](https://github.com/Azure-Samples/ms-identity-python-samples-common)
 * [Demo](https://github.com/azure-samples/ms-identity-b2c-python-flask-webapp-authentication)


### Auth errors

    
    File "/Users/michiel/Coding/MSALTest/venv/lib/python3.9/site-packages/msal/authority.py", line 83, in __init__
    openid_config = tenant_discovery(
    File "/Users/michiel/Coding/MSALTest/venv/lib/python3.9/site-packages/msal/authority.py", line 151, in tenant_discovery
            return payload  # Happy path
        raise ValueError("OIDC Discovery does not provide enough information")

    if 400 <= resp.status_code < 500:
        # Nonexist tenant would hit this path
        # e.g. https://login.microsoftonline.com/nonexist_tenant/v2.0/.well-known/openid-configuration
        raise ValueError("OIDC Discovery endpoint rejects our request")

    # Transient network error would hit this path
    resp.raise_for_status()
    raise RuntimeError(  # A fallback here, in case resp.raise_for_status() is no-op
        "Unable to complete OIDC Discovery: %d, %s" % (resp.status_code, resp.text))

## Django

...
