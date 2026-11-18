from flask import Blueprint, request
from flask_restful import Resource
from pydantic import ValidationError
from app.schemas.usersxm import UserCreateSchemas,UserUpdateSchemas
from app.models.user import User
from app.models import db
from pydantic import BaseModel,Field
from app.routes.decorators import role_required
from flask_bcrypt import generate_password_hash,check_password_hash


user_bp=Blueprint('users',__name__,url_prefix='/users')

class UserResource(Resource):

    def get(self,user_id):
        user=User.query.filter_by(id=user_id).first()
        if user is None:
            return {"message":"Bunday idli user yuq"},404
        return{
            "users":[{
                "id":user.id,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "username":user.username,
                "password":user.password,
            }]
        },200

    def delete(self,user_id):
        user=User.query.filter_by(id=user_id).first()
        if user is None:
            return {"message":"Bunday idli user yuq"},404
        db.session.delete(user)
        db.session.commit()
        return {"message":"User muvaffqaiyatli uchirildi"},200

    def patch(self,user_id):
        try:
            data=UserUpdateSchemas.model_validate(request.get_json())
            password_hash=generate_password_hash(data.password).decode('utf-8')
            user=User.query.filter_by(id=user_id).first()
            if user is None:
                return {"message":"Bunday idli user yuq"},404
            if data.first_name is not None:
                user.first_name=data.first_name
            if data.last_name is not None:
                user.last_name =data.last_name
            if data.username is not None:
                user.username=data.username
            if data.password is not None:
                user.password=password_hash
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return{"message":"User muvaffaqiyatli yangilandi","user":user._dict()},200

    def put(self,user_id):
        try:
            data=UserUpdateSchemas.model_validate(request.get_json())
            password_hash=generate_password_hash(data.password).decode('utf-8')
            user=User.query.filter_by(id=user_id).first()
            if user is None:
                return {"message":"Bunday idli user yuq"},404
            user.first_name=data.first_name
            user.last_name=data.last_name
            user.username=data.username
            user.password=password_hash
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return{"message":"User muvaffaqiyatli tuliq yangilandi","user":user._dict()},200

class UserCreateResource(Resource):
    @role_required(['admin'])
    
    def get(self):
        users=User.query.all()
        return({
            "users":[user._dict() for user in users]},200)

    
    @role_required(['admin'])
    def post(self):
        try:
            data=UserCreateSchemas.model_validate(request.get_json())
            password_hash=generate_password_hash(data.password).decode('utf-8')

            new_user=User(
                first_name=data.first_name,
                last_name=data.last_name,
                username=data.username,
                
                password=password_hash)
            
            db.session.add(new_user)
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return{"message":"User muvaffqaiyatli yaratildi","user":new_user._dict()},201
    
