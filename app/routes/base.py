from flask import Blueprint
from flask_bcrypt import generate_password_hash ,check_password_hash
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity

from app.models import User,db

base_bp=Blueprint("base",__name__)

@base_bp.route("/profile")
@jwt_required()
def profile():
    id = int(get_jwt_identity())
    user: User = User.query.filter_by(id=id).first()
    return {"message": user._dict()}
    