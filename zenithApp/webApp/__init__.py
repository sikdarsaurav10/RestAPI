from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webApp.config import Config
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

import webApp.routes
from webApp.postapi.views import post
from webApp.cabapi.routes import cab
from webApp.restrauntapi.routes import food
from webApp.suppportapi.routes import support
from webApp.applicationapi.routes import permission

app.register_blueprint(post, url_prefix="/post")
app.register_blueprint(cab, url_prefix="/cab")
app.register_blueprint(food, url_prefix="/food")
app.register_blueprint(support, url_prefix="/support")
app.register_blueprint(permission, url_prefix="/permission")
