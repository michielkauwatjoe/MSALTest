# Django MSAL

Implements sign on part of (skipping calendar event parts):

* https://docs.microsoft.com/en-us/graph/tutorials/python

A `oauth_settings.yml` file needs to be added next to manage.py:

    app_id: "<your-app-id>"
    app_secret: "<your-secret-key>"
    redirect: "http://localhost:5000/getAToken"
    scopes:
      - user.read
      # more scopes can be added here.
    authority: "https://login.microsoftonline.com/<tenant-id>"


