from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models import db
from .config import Config
from .routes import main, user


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
app.register_blueprint(main.bp)
app.register_blueprint(user.bp)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
