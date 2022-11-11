from flask import Blueprint, request,jsonify

from api import db

from api.models import User, School, Game
from api.route.auth import login_required
import datetime

bp = Blueprint('qr', __name__, url_prefix='/qr')


@bp.route('/<string:user_id>', methods=["GET"])
@login_required
def qr(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({
            "code": -1,
            "msg": "존재하지 않는 사용자",
        })
    return jsonify({
        "code": 1,
        "msg": "qr 반환",
        "qr": user.qr
    })


@bp.route('/cam/<string:code>', methods=["GET"])
# @login_required
def qr_check(code):
    user = User.query.filter_by(qr=code).first()
    school = School.query.filter_by(school_code=user.school_code).first()
    now = datetime.datetime.now()

    if now.time() < school.school_time:
        game = Game.query.filter_by(user_id=user.user_id).first()
        game.exp += int(game.max_exp * 0.1)
        game.point += 100
        db.session.commit()
        data = {
            "exp": int(game.max_exp * 0.1),
            "point": 100
        }
        db.session.remove()

        return jsonify({
            "code" : 1,
            "msg" : [f"{data['exp']} 경험치 획득!", f"{data['point']}포인트 획득!"]
        })



