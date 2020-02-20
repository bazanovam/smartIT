from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config, DevelopementConfig

bootstrap = Bootstrap()
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
#config_name = 'development'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    print(config_name)
    #app.config.from_object(config[config_name])
    app.config.from_object(DevelopementConfig) 
    #app.config.from_envvar('de')
    #app.config.from_pyfile('./config.py')
    DevelopementConfig.init_app(app)
    

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .issue import issue as issue_blueprint
    app.register_blueprint(issue_blueprint)

    from .request import request as request_blueprint
    app.register_blueprint(request_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
