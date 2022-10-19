from flask import request, jsonify, Response, json, Blueprint

from api import db
from api.models import User, School

import bcrypt, jwt
from config import JWT_SECRET_KEY
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
        })
    else:
        return jsonify({
            'code': 0,
            'msg': "학교코드가 잘못되었거나 아이디가 사용중입니다.",
            'data': {}
        })

@bp.route('/login/', methods=['POST'])
def login():
    error = None
    user = User.query.filter_by(user_id = request.json["user_id"]).first()

    if not user:
        error = "존재하지 않는 사용자입니다."
    elif not bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password.encode('utf-8')):
        error = "비밀번호가 올바르지 않습니다."

    if error is None:
        payload = {
            "user_id" : user.user_id,
            "username" : user.username,
            "password" : user.password
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        body = json.dumps({
            "code": 1,
            "msg": "로그인에 성공하셨습니다.",
            "data": {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "user_id": user.user_id
            }
        }, ensure_ascii=False)

        db.session.remove()
        response = Response(body)
        response.headers['authorization'] = token
        return response

    return jsonify({
        "code": -1,
        "msg": error,
    })
# http -v POST http://43.201.142.6:5000/auth/singnup/ user_id="test" username="홍길동" password="test1234" email="test@naver.com" job="학생" school_code='qV8ugGBVT3'