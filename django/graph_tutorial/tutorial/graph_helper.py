import requests
import json

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
    endpoint = '{0}/me'.format(graph_url)
    params = {'$select': 'displayName,mail,userPrincipalName'}
    #params = {'$select': 'displayName,mail,mailboxSettings,userPrincipalName'}
    headers = {'Authorization': 'Bearer {0}'.format(token)}

    # Send GET to /me
    user = requests.get(endpoint, headers=headers, params=params)
    return user.json()
