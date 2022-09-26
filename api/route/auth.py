from flask import request, jsonify, Response, json, Blueprint

from api import db
from api.models import User, School

import bcrypt, jwt
# from config import JWT_SECRET_KEY, IS_CAM_KEY
from functools import wraps
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth') # URL과 함수의 매핑을 관리하기 위해 사용하는 도구(클래스)


@bp.route('/singnup/', methods=['POST'])
def singnup():
    user = User.query.filter_by(user_id = request.json["user_id"]).first()
    school = School.query.filter_by(school_code = request.json["school_code"]).first()
    if not user and school:
        user_id = request.json["user_id"]
        username = request.json["username"]
        password = bcrypt.hashpw(request.json['password'].encode("utf-8"), bcrypt.gensalt())
        email = request.json["email"]
        job = request.json["job"]
        school_code = school.school_code

        user = User(user_id = user_id,
                    username = username,
                    password = password.decode('utf-8'),
                    email = email,
                    job = job,
                    school_code = school_code)
        db.session.add(user)
        db.session.commit()
        db.session.remove()

        return jsonify({
            'code': 1,
            'msg': "회원가입 성공!",
            'data': {}
        })
    else:
        return jsonify({
            'code': 0,
            'msg': "학교코드가 잘못되었거나 아이디가 사용중입니다.",
            'data': {}
        })


# http -v POST http://127.0.0.1:5000/auth/singnup/ user_id="test", username="홍길동", password="test1234", email="test@naver.com", job="학생", school_code="없음"