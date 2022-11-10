import datetime

from flask import request, jsonify, Response, json, Blueprint

import making_code
from api import db
from api.models import User, SchoolClass, Game
import bcrypt, jwt
from config import JWT_SECRET_KEY
from functools import wraps

from email_validator import validate_email, EmailNotValidError

bp = Blueprint('auth', __name__, url_prefix='/auth') # URL과 함수의 매핑을 관리하기 위해 사용하는 도구(클래스)


@bp.route('/singnup/', methods=['POST'])
def singnup():
    user = User.query.filter_by(user_id = request.json["user_id"]).first()
    check_code = SchoolClass.query.filter_by(school_code = request.json["school_code"]).filter_by(class_code = request.json["class_code"]).first()
    error = None
    if user:
        error = "아이디가 사용중입니다."
    elif not check_code:
        error = "코드가 잘못되었습니다."
    elif not check_email(request.json["email"]):
        error = "이메일이 잘못되었습니다."

    if error is None:
        user_id = request.json["user_id"]
        username = request.json["username"]
        password = bcrypt.hashpw(request.json['password'].encode("utf-8"), bcrypt.gensalt())
        email = request.json["email"]
        # job = request.json["job"]
        school_code = check_code.school_code
        class_code = check_code.class_code
        try:
            isStudent = request.json["isStudent"]
        except KeyError:
            isStudent = False
        user = User(user_id = user_id,
                    username = username,
                    password = password.decode('utf-8'),
                    email = email,
                    isStudent = isStudent,
                    school_code = school_code,
                    class_code= class_code)
        game = Game(
            user_id=user_id,
            username=username
        )
        db.session.add(user)
        db.session.add(game)
        db.session.commit()
        db.session.remove()

        return jsonify({
            'code': 1,
            'msg': "회원가입 성공!",
        })
    else:
        return jsonify({
            'code': -1,
            'msg': error,
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
        game = Game.query.filter_by(user_id=user.user_id).first()
        body = json.dumps({
            "code": 1,
            "msg": "로그인에 성공하셨습니다.",
            "data": {
                "id": user.id,
                "username": user.username,
                "user_id": user.user_id,
                "isStudent": user.isStudent,
                "class_code": user.class_code,
                "school_code": user.school_code,
                "level": game.level,
                "exp": game.exp,
                "max_exp": game.max_exp,
                "point": game.point
            }
        }, ensure_ascii=False)

        user.qr = making_code.make_qr()
        db.session.commit()

        db.session.remove()
        response = Response(body)
        response.headers['authorization'] = token
        return response

    return jsonify({
        "code": -1,
        "msg": error,
    })

def check_email(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError as e:
        return False


def check_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, "HS256")
    except jwt.InvalidTokenError:
        payload = None
    return payload


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwagrs):
        token = request.headers.get('authorization')
        if token is not None:
            payload = check_token(token)
            if payload is None:
                return jsonify({
                    "code" : -1,
                    "msg" : "토큰 검증에 실패하셨습니다."
                })
        else:
            return jsonify({
                "code": -1,
                "msg": "토큰 검증에 실패하셨습니다."
            })
        return f(*args, **kwagrs)
    return decorated_function
# http -v POST http://127.0.0.1:5000/auth/singnup/ user_id="test3" username="티쳐" password="test1234" email="teacher@naver.com" school_code='qV8ugGBVT3'
# http -v POST http://43.201.142.6:5000/auth/singnup/ user_id="test3" username="티쳐" password="test1234" email="teacher@naver.com" school_code='qV8ugGBVT3'