from flask import Flask, Blueprint
from flask_migrate import Migrate
from .models import db, ma
from .views.UserView import user_bp
from .views.BlogpostView import blogpost_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(blogpost_bp, url_prefix='/blogposts')

    @app.route('/')
    def root():
        return { 'message': 'hello from root route' }

    return app
