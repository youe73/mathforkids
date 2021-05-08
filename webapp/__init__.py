from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path
from flask_login import LoginManager
import urllib
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy() 
DB_NAME = "sqlitedatabase.db"
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # for login_required object used as a decorater
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY        
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI 
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)        
        
    from .parents import parents
    from .auth import auth
    from .kids import kids
      
    app.register_blueprint(parents, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')  
    app.register_blueprint(kids, url_prefix='/') 

    from .models import Users

    create_database(app)   
    
    

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))


    return app


def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app=app)
        print('Database created!')
