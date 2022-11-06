from flask import Blueprint, request,jsonify

from api import db

from api.models import User, Notice
from api.route.auth import login_required
import datetime

bp = Blueprint('notice', __name__, url_prefix='/notice')

@bp.route("/app/<string:teacher_id>", methods=['GET','POST'])
@login_required
def app_notice(teacher_id):
    user = User.query.filter_by(user_id=teacher_id).first()
    if user.isStudent == False:
        if request.method == "POST":
            notice = Notice(
                title=request.json['title'],
                content=request.json['content'],
                current_date=datetime.datetime.strptime(request.json['current_date'], '%Y-%m-%d'),
                teacher_id=teacher_id,
                class_code=request.json['class_code']
            )
            db.session.add(notice)
            db.session.commit()
            db.session.remove()
            return jsonify({
                "code": 1,
                "msg": "공지사항 추가 성공!",
            })
        elif request.method == "GET":
            notice = Notice.query.filter_by(teacher_id=teacher_id)
            notice = serializable_Notice(notice)
            db.session.remove()
            return jsonify({
                "code": 1,
                "msg": "공지사항 목록 반환!",
                "data": notice
            })

    else:
        return jsonify({
            "code": -1,
            "msg": "학생은 사용할 수 없는 서비스입니다.",
        })


@bp.route("/game/<string:user_id>", methods=['GET'])
@login_required
def game_notice(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    notice = Notice.query.filter_by(class_code=user.class_code)
    notice = serializable_Notice(notice)
    return jsonify({
        "code": 1,
        "msg": "공지사항 목록 반환!",
        "data": notice
    })


def serializable_Notice(info_list):
    lst = []
    for info in info_list:
        lst.append(
            {
                "id": info.id,
                "title": info.title,
                "content": info.content,
                "current_date": info.current_date.strftime('%Y-%m-%d'),
                "teacher_id": info.teacher_id,
                "class_code": info.class_code
            }
        )
    return lst