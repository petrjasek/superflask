import flask
import mongoengine

import superdesk.types
import superdesk.resources

mongoengine.connect('superdesk')

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.register_blueprint(superdesk.types.get_blueprint(), url_prefix='/api')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/')
def index():
    """Return list of registered urls."""

    rules = []
    for rule in app.url_map.iter_rules():
        rules.append(str(rule))
    response = flask.jsonify({'urls': rules})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run()
