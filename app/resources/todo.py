from flask import Blueprint, request
from flask_restful import Resource
from pydantic import ValidationError
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.schemas.todosxm import TodoCreateSchemas,TodoUpdateSchemas
from flask_jwt_extended import jwt_required
from app.models.todo import Todo
from app.models import db
from pydantic import BaseModel,Field
from app.routes.decorators import role_required

todo_bp=Blueprint("todos",__name__,url_prefix="/todos")

class TodoResource(Resource):
    @jwt_required()
    def get(self,todo_id):
        todo=Todo.query.filter_by(id=todo_id, user_id=int(get_jwt_identity())).first()
        if todo is None:
            return{"message":"Bunday idli todo yuq"},404
        return{
            "todos":[{
                "id":todo.id,
                "title":todo.title,
                "description":todo.description
            }]
        }

    
    @jwt_required()
    def delete(self,todo_id):
        todo=Todo.query.filter_by(id=todo_id,user_id=int(get_jwt_identity())).first()
        if todo is None:
            return{"message":"Bunday idli todo yuq"},404
        db.session.delete(todo)
        db.session.commit()
        return{"message":"Todo muvaffaqiyatli uchirildi"},200

    @jwt_required()
    def patch(self,todo_id):
        try:
            data=TodoUpdateSchemas.model_validate(request.get_json())
            todo=Todo.query.filter_by(id=todo_id,user_id=int(get_jwt_identity())).first()
            if todo is None:
                return{"message":"Bunday idli todo yuq"},404
            if data.title is not None:
                todo.title=data.title
            if data.description is not None:
                todo.description=data.description
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return {"message":"Todo muvaffaqiyatli yangilandi","todo":todo._dict()},200

    @jwt_required()
    def put(self,todo_id):
        try:
            data=TodoUpdateSchemas.model_validate(request.get_json())
            todo=Todo.query.filter_by(id=todo_id,user_id=int(get_jwt_identity())).first()
            if todo is None:
                return{"message":"Bunday idli todo yuq"},404
            todo.title=data.title
            todo.description=data.description
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return{"message":"Todo muvaffaqiyatli tuliq yangilandi","todo":todo._dict()},200

class TodoCreateResource(Resource):
    @jwt_required()
    def get(self):
        todos=Todo.query.filter_by(user_id=int(get_jwt_identity())).all()
        return({
            "todos":[todo._dict() for todo in todos]},200)

    @jwt_required()
    def post(self):
        try:
            data=TodoCreateSchemas.model_validate(request.get_json())
            user_id = int(get_jwt_identity())

            new_todo = Todo(
            title=data.title,
            description=data.description,
            user_id=user_id)
            db.session.add(new_todo)
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)},200
        return{"message":"Todo muvaffqiyatli yaratildi","todo":new_todo._dict()},201


    

class TodoAdminResource(Resource):
    @role_required(['admin'])
    @jwt_required()
    def get(self,todo_id):
        todo=Todo.query.filter_by(id=todo_id).first()
        if todo is None:
            return{"message":"Bunday idli todo yuq"},404
        return{
            "todos":[{
                "id":todo.id,
                "title":todo.title,
                "description":todo.description
            }]
        }

    @role_required(['admin'])
    def delete(self,todo_id):
        todo=Todo.query.filter_by(id=todo_id).first()
        if todo is None:
            return{"message":"Bunday idli todo yuq"},404
        db.session.delete(todo)
        db.session.commit()
        return{"message":"Todo muvaffaqiyatli uchirildi"},200

    @role_required(['admin'])
    def patch(self,todo_id):
        try:
            data=TodoUpdateSchemas.model_validate(request.get_json())
            todo=Todo.query.filter_by(id=todo_id).first()
            if todo is None:
                return{"message":"Bunday idli todo yuq"},404
            if data.title is not None:
                todo.title=data.title
            if data.description is not None:
                todo.description=data.description
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return {"message":"Todo muvaffaqiyatli yangilandi","todo":todo._dict()},200

    @role_required(['admin'])
    def put(self,todo_id):
        try:
            data=TodoUpdateSchemas.model_validate(request.get_json())
            todo=Todo.query.filter_by(id=todo_id).first()
            if todo is None:
                return{"message":"Bunday idli todo yuq"},404
            todo.title=data.title
            todo.description=data.description
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return{"message":"Todo muvaffaqiyatli tuliq yangilandi","todo":todo._dict()},200




class TodoAdminCreateResource(Resource):
    @jwt_required()
    @role_required(['admin'])
    def get(self):
        todos=Todo.query.all()
        return({"todos":[todo._dict() for todo in todos]},200)

    @role_required(['admin'])
    def post(self):
        try:
            data=TodoCreateSchemas.model_validate(request.get_json())
            user_id = int(get_jwt_identity())

            new_todo = Todo(
            title=data.title,
            description=data.description,
            user_id=user_id)

            db.session.add(new_todo)
            db.session.commit()
        except ValidationError as e:
            return {"errors":e.errors(include_url=False)}
        return{"message":"Todo muvaffqiyatli yaratildi","todo":new_todo._dict()},201
