# quattro_scelte/__init__.py        2022/04/25  M.O
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=False):

    app = Flask(__name__)

    app.config.from_object('quattro_scelte.config')

    if test_config:
        app.config.from_mapping(test_config)

    from quattro_scelte.views import views
    app.register_blueprint(views)

    db.init_app(app)
    migrate.init_app(app, db)

    return app

