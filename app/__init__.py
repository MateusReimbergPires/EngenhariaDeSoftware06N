from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('../config.py')
    
    db.init_app(app)
    bcrypt.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app