from flask import Flask
from config import Config
from models import db
from flask_restx import Api

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize Flask-RESTX
api = Api(app, doc='/docs')  # Swagger UI will be available at /docs

# Import the API namespaces
from api.user import api as user_ns
from api.job_title import api as job_title_ns
from api.skill import api as skill_ns

# Add the namespaces to the API
api.add_namespace(user_ns, path='/users')
api.add_namespace(job_title_ns, path='/job_titles')
api.add_namespace(skill_ns, path='/skills')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
