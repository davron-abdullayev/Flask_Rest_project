
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity,jwt_required

from app.models.user import User

def role_required(role_list:list):
    def decorator(func):
        @jwt_required()
        @wraps(func)
        def wrapped(*args,**kwargs):
            id=get_jwt_identity()
            user=User.query.filter_by(id=id).first()
            print("User role:", user.is_role)
            print("Allowed roles:", role_list)

            if not user:
                return jsonify({"message":"Bunday user mavjud emas"}),404

            if user.is_role.value not in role_list:
                return jsonify({"message":"Sizga bu pagega ruxsat yuq"},403)
            return func(*args,**kwargs)
        return wrapped
    return decorator
 