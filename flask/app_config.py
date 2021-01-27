import os

# Application (client) ID of app registration.
CLIENT_ID = ""

# NOTE: this is a placeholder secret - for use ONLY during testing!
CLIENT_SECRET = ""

# In a production app, we recommend you use a more secure method of storing
# your secret, like Azure Key Vault. Or, use an environment variable as
# described in Flask's documentation:
# * https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/<tenant-name>"

# Used for forming an absolute URL to your redirect URI. The absolute URL must
# match the redirect URI you set in the app's registration in the Azure portal.
REDIRECT_PATH = "/getAToken"

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer

# This resource requires no admin consent.
BASEURI = 'https://graph.microsoft.com/v1.0'

# Available endpoints.
ENDPOINTME = '%s/me' % BASEURI
ENDPOINTUSERS = '%s/users' % BASEURI
ENDPOINTGROUPS = '%s/groups' % BASEURI
ENDPOINTAPP = '%s/applications' % BASEURI

# You can find the proper permission names from this document here:
# * https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["Application.Read.All"]
SCOPEGROUP = ["Group.Read.All",]
SCOPEAPP = ["Application.Read.All",]
#SCOPEROLES = ["AppRoleAssignment.ReadWrite.All",]

# Specifies the token cache should be stored in server-side session.
SESSION_TYPE = "filesystem"
