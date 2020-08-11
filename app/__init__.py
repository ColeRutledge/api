from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.config import Config
from app.routes import bp
# from app.forms import form


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(bp)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
