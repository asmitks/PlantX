# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import urllib.parse 
from flask import Flask
import pyodbc
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

server = 'tcp:plantx.database.windows.net'
database = 'PlantX'
username = 'Atishay'
password = 'DBMSproject123'
driver= '{ODBC Driver 17 for SQL Server}'
params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

def create_app():
    app = Flask(__name__)
    print("SADDDDDDDDDDDDDD")

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    # conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    print("SADDDDDDDDDDDDDD")
    db.init_app(app)
    print("SADDDDDDDDDDDDDDS")

    from .models import Users
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Users.query.get(user_id)
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app