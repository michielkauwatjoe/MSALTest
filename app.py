from ms_identity_web import IdentityWebPython
from ms_identity_web.adapters import FlaskContextAdapter
from ms_identity_web.configuration import AADConfig

adapter = FlaskContextAdapter(app)    # we are using flask
ms_identity_web = IdentityWebPython(AADConfig.parse_json('aad.config.json'), adapter) # instantiate utils

@app.route('/my_protected_route')
@ms_identity_web.login_required # <-- developer only needs to hook up this decorator to any login_required endpoint like this
def my_protected_route():
    return render_template('my_protected_route.html')

