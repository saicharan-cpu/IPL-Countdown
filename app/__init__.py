from flask import Flask

from app.api import setup_database
from app.config import DB_CONFIG


def create_app():
    app = Flask(__name__)
    app.config['DB_CONFIG'] = DB_CONFIG
    from .api import configure_routes
    setup_database(app)
    configure_routes(app)

    return app

