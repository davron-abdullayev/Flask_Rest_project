from flask import Flask
from .auth import auth_bp
from .base import base_bp
from ..resources.todo import todo_bp


def register_bp(app:Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(base_bp)
    app.register_blueprint(todo_bp)
   
    