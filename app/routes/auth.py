
from flask import Blueprint,current_app,jsonify,request
from flask_bcrypt import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.schemas.usersxm import UserLoginSchemas,UserRegisterSchemas
from app.models.user import User,db
from pydantic import ValidationError

auth_bp=Blueprint("auth",__name__,url_prefix='/auth')

@auth_bp.post("/register")
def register():
    try:
        data=UserRegisterSchemas.model_validate(request.get_json())
    except ValidationError as e:
        return {"errors":e.errors(include_url=False)},400
    first_name=data.first_name
    last_name=data.last_name
    username=data.username
    password=data.password

    password_hash=generate_password_hash(password).decode('utf-8')
    user=User.query.filter_by(username=username).first()

    if user:
        current_app.logger.warning("Bunday user allaqachon mavjud"),200
        return jsonify ({"message": "Bunday user allaqachon mavjud"})

    new_user=User(first_name=first_name,last_name=last_name,username=username,password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    token=create_access_token(identity=str(new_user.id))
    current_app.logger.info("User royhatdan utdi",201)
    return jsonify ({"message":"User ro'yhatdan o'tdi","token":token},200)



@auth_bp.post("/login")
def login():
    data=UserLoginSchemas.model_validate(request.get_json())
    username=data.username
    password=data.password

    user=User.query.filter_by(username=username).first()

    if not check_password_hash(user.password,password) or not user:
        current_app.logger.warning("Parol yoki username nato'g'ri",200)
        return jsonify({"message":"Parol yoki username nato'g'ri"})
    token=create_access_token(identity=str(user.id))
    current_app.logger.info("User login qildi")
    return jsonify ({"message":"User login qildi","token":token})

@auth_bp.get("/me")
@jwt_required()
def profile():
    id=int(get_jwt_identity())
    user:User=User.query.filter_by(id=id).first()
    return  jsonify ({"user":user._dict()},200)