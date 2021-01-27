#!/usr/bin/env python3
import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

CACHE_KEY = "token_cache"

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)

@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.SCOPE, state=session["state"])
    return render_template("login.html", auth_url=auth_url, version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache(CACHE_KEY)
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized", _external=True))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache, CACHE_KEY)
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route("/users")
def users():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))

    # Calls requests and uses a token to call the downstream service.
    graph_data = requests.get(
        app_config.ENDPOINTUSERS,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()

    return render_template('display.html', result=graph_data)

@app.route("/groups")
def groups():
    # https://docs.microsoft.com/en-us/graph/api/group-list-approleassignments?view=graph-rest-1.0&tabs=http
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))

    graph_data = requests.get(
        app_config.ENDPOINTGROUPS,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()

    return render_template('display.html', result=graph_data)

@app.route("/app")
def application():
    # https://docs.microsoft.com/en-us/graph/api/group-list-approleassignments?view=graph-rest-1.0&tabs=http
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))

    ep = '%s/%s' % (app_config.ENDPOINTAPP, '?$count=true')
    graph_data = requests.get(
        ep,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()

    print(graph_data)
    return render_template('display.html', result=graph_data)

def _get_token_from_cache(scope=None, cacheKey=None):
    cacheKey = cacheKey or CACHE_KEY
    # TODO: store tokens for various scope levels?
    cache = _load_cache(cacheKey)  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache, cacheKey)
        return result

def _load_cache(cacheKey):
    # TODO: store tokens for various scope levels?
    cache = msal.SerializableTokenCache()
    if session.get(cacheKey):
        cache.deserialize(session[cacheKey])
    return cache

def _save_cache(cache, cacheKey):
    # TODO: store tokens for various scope levels?
    if cache.has_state_changed:
        session[cacheKey] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))

app.jinja_env.globals.update(_build_auth_url=_build_auth_url)  # Used in template

if __name__ == "__main__":
    app.run()
