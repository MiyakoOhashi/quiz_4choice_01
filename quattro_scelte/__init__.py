# quattro_scelte/__init__.py        2022/04/25  M.O
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.login_message = 'ログインしてください'

def create_app(test_config=False):

    app = Flask(__name__)

    app.config.from_object('quattro_scelte.config')

    if test_config:
        app.config.from_mapping(test_config)

    from quattro_scelte.views import views
    app.register_blueprint(views)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)

    login_manager.init_app(app)

    return app

