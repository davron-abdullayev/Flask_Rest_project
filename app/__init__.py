
from flask import Flask 
from flask_restful import Api 
from .routes import register_bp
import logging
from logging.handlers import RotatingFileHandler
from app.routes.auth import auth_bp
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from app.resources.main import UserCreateResource,UserResource
from app.resources.todo import TodoCreateResource,TodoResource,TodoAdminCreateResource,TodoAdminResource


def get_error(message,result,status_code):
    return{"message":message,"result":result,"status_code":status_code}






from .models import db,bcrypt,migrate,jwt
def create_app():
    app=Flask(__name__)
    
    file_handler=RotatingFileHandler("main.log")
    file_handler.setLevel(logging.INFO)


    formatter=logging.Formatter(
        "%(asctime)s- %(levelname)s-%(message)s",datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


    @app.errorhandler(404)
    def error_404(error):
        return get_error("Page not found",None,404)
    
    api=Api(app)

    api.add_resource(UserCreateResource,"/users/")
    api.add_resource(UserResource,"/users/<int:user_id>")
    api.add_resource(TodoCreateResource,"/todos/")
    api.add_resource(TodoResource,"/todos/<int:todo_id>")
    api.add_resource(TodoAdminCreateResource,"/admin/todos/")
    api.add_resource(TodoAdminResource,"/admin/todos/<int:todo_id>")

    app.config['SECRET_KEY']='jhdgajhvfdsahjvhmcdbj'

    app.config['SQLALCHEMY_DATABASE_URI']=(
    "postgresql://postgres:davron5021@localhost:5432/flask_rest")

    app.config["WTF_CSRF_SECRET_KEY"]='yugduyejwgduhjghebdws'

    app.config["JWT_ACCESS_TOKEN_EXPIRES"]=3600 


    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app,db)
   


    register_bp(app)

    return app

