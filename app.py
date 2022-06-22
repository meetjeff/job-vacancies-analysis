from flask import Flask
from flask_restful import Api
from apis import trigger,status,skill,location,jobtitle,enterprise,salary,website
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask import render_template

app = Flask(__name__)
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Career Project API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/api'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

@app.route('/')
def index():
    return render_template('view.html')

api.add_resource(trigger,'/crawlertrigger/<string:website>/<string:search>/<int:page>')
docs.register(trigger)
api.add_resource(status,'/status/<string:website>')
docs.register(status)
api.add_resource(skill,'/skill/<string:skill>/<int:records>')
docs.register(skill)
api.add_resource(location,'/location/<string:location>/<int:records>')
docs.register(location)
api.add_resource(jobtitle,'/jobtitle/<string:jobtitle>/<int:records>')
docs.register(jobtitle)
api.add_resource(enterprise,'/enterprise/<string:enterprise>/<int:records>')
docs.register(enterprise)
api.add_resource(salary,'/salary/<int:salary>/<int:records>')
docs.register(salary)
api.add_resource(website,'/website/<string:website>/<int:records>')
docs.register(website)


if __name__ == '__main__':
    app.run()
