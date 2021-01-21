# MSALTest

## Flask

    cd <project-root-directory>
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ./run.sh
    
Should start the server at:

 * [localhost:5000](https://127.0.0.1:5000)

 Config:


 * client_id == secret key
 * client_credential == 
 * authority == Tenant ID
 
 Something like:
 
 
     "authority": "https://<tenantname>.b2clogin.com/<tenantname>.onmicrosoft.com"
 
 See also:
 
  * https://docs.microsoft.com/en-us/azure/active-directory-b2c/tutorial-create-tenant


See also:

 * [Py examples](https://github.com/Azure-Samples/ms-identity-python-samples-common)
 * [Demo](https://github.com/azure-samples/ms-identity-b2c-python-flask-webapp-authentication)


## Django

...
