from flask import Flask
from flask_bcrypt import Bcrypt
from .views import views
from .auth import auth

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'casavet 4101'
    
    
    
    bcrypt.init_app(app) 
    app.bcrypt = bcrypt
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app


    