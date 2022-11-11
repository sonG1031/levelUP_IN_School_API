from flask import Blueprint, request,jsonify

import making_code
from api import db

from api.models import User, School, Game
from api.route.auth import login_required
import datetime

bp = Blueprint('qr', __name__, url_prefix='/qr')


@bp.route('/<string:user_id>', methods=["GET"])
@login_required
def qr(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    qr_ = user.qr
    db.session.remove()
    return jsonify({
        "code": 1,
        "msg": "qr 반환",
        "qr": qr_
    })


@bp.route('/updateExp/<string:user_id>', methods=["GET"])
@login_required
def update_exp(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    game = Game.query.filter_by(user_id=user.user_id).first()
    exp = game.exp
    level = game.level
    max_exp = game.max_exp
    point = game.point

    return jsonify({
        "exp" : exp,
        "level" : level,
        "max_exp" : max_exp,
        "point" : point
    })


@bp.route('/cam/<string:code>', methods=["GET"])
# @login_required
def qr_check(code):
    user = User.query.filter_by(qr=code).first()
    school = School.query.filter_by(school_code=user.school_code).first()
    now = datetime.datetime.now()

    if now >= user.qr_date + datetime.timedelta(hours=24):
        user.qr_checked = False
        user.qr = making_code.make_qr()
        user.qr_date = datetime.datetime.now()
        db.session.commit()
        db.session.remove()

        return jsonify({
            "code" : 1,
            "msg" : "QR 초기화"
        })
    if user.qr_checked == False and now.time() < school.school_time:
        game = Game.query.filter_by(user_id=user.user_id).first()
        game.exp += int(game.max_exp * 0.2)
        game.point += 100
        user.qr_checked = True
        db.session.commit()
        data = {
            "exp": int(game.max_exp * 0.2),
            "point": 100
        }
        db.session.remove()

        return jsonify({
            "code" : 1,
            "msg" : [f"{data['exp']} 경험치 획득!", f"{data['point']}포인트 획득!"]
        })
    else:
        return jsonify({
            "code": -1,
            "msg": "이미 qr인식함 ㅅㄱ"
        })



