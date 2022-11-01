from flask import Blueprint, request,jsonify
from api import db

from api.models import Quest, User, Game
from api.route.auth import login_required
import datetime

bp = Blueprint('quest', __name__, url_prefix='/quest')


@bp.route("/app/<string:teacher_id>", methods=["GET", "POST"])
@login_required
def app_quest(teacher_id): # 자신이 생성한 퀘스트 보기(GET), 퀘스트 추가하기(POST)
    user = User.query.filter_by(user_id = teacher_id).first()
    if user.job == "교사":
        if request.method == 'POST':
            title = request.json['title']
            description = request.json['description']
            exp = request.json['exp']
            start_date = request.json['start_date']
            end_date = request.json['end_date']
            point = request.json['point']
            class_code = request.json['class_code']
            # teacher_id = request.json['teacher_id']

            user_lst = User.query.filter_by(class_code = class_code)
            quest_lst = []
            for user in user_lst:
                quest_lst.append(Quest(
                    title = title,
                    description = description,
                    exp = exp,
                    start_date = start_date,
                    end_date = end_date,
                    point = point,
                    user_id = user.user_id,
                    teacher_id = teacher_id
                ))
            for data in quest_lst:
                db.session.add(data)
            db.session.commit()
            db.session.remove()

            return jsonify({
                "code": 1,
                "msg": "퀘스트 추가 완료!",
            })
        elif request.method == 'GET':
            quest_lst = Quest.query.filter_by(teacher_id=teacher_id)
            quest_lst = get_infoList(quest_lst)
            db.session.remove()

            return jsonify({
                "code": 1,
                "msg": "퀘스트 목록 반환!",
                "data": quest_lst
            })
    else:
        return jsonify({
            "code": -1,
            "msg": "학생은 사용할 수 없는 서비스입니다.",
        })


@bp.route("/app/check/<string:teacher_id>", methods=['POST'])
@login_required
def app_check(teacher_id):
    user = User.query.filter_by(user_id=teacher_id).first()
    if user.job == "교사":
        q = Quest.query.filter((Quest.user_id == request.json['user_id']) | (Quest.id == request.json['quest_id'])).first()
        q.check = True
        db.session.commit()
        db.session.remove()
        return jsonify({
            "code": 1,
            "msg": "퀘스트 완료 요청을 수락하였습니다.",
        })


@bp.route("/game/<string:user_id>", methods=["GET", "POST"])
@login_required
def game_quest(user_id): # 자신의 퀘스트 목록 가져오기(GET), 퀘스트 완료요청 보내기(POST)
    if request.method == "GET":
        now = datetime.datetime.now()
        user_quest = Quest.query.filter((Quest.user_id == user_id) | (Quest.start_date <= now <= Quest.end_date))
        user_quest = get_infoList(user_quest)
        db.session.remove()
        return jsonify({
            "code": 1,
            "msg": "유저 퀘스트 목록 반환!",
            "data": user_quest
        })
    elif request.method == "POST":
        user_quest = Quest.query.filter((Quest.user_id == user_id) | (Quest.id == request.json['quest_id'])).first()
        now = datetime.datetime.now()

        if user_quest.create_date > now:
            return jsonify({
                "code": -1,
                "msg": "퀘스트가 아직 활성화되지 않았습니다.",
            })
        elif user_quest.end_date < now:
            db.session.delete(user_quest)
            db.session.remove()
            return jsonify({
            "code": -1,
            "msg": "퀘스트 기간이 만료되었습니다.",
            })
        else:
            user_quest.done = True
        db.session.commit()
        db.session.remove()
        return jsonify({
            "code": 1,
            "msg": "퀘스트 완료 요청을 보냈습니다.",
        })


@bp.route('/game/reward/', methods=['POST'])
def game_reward():
    game_info = Game.query.filter_by(user_id=request.json['user_id']).first()
    reward_info = Quest.query.filter((Quest.user_id == request.json['user_id']) | (Quest.id == request.json['quest_id'])).first()
    game_info.point += reward_info.point
    game_info.exp += reward_info.exp

    db.session.delete(reward_info) # 퀘스트를 완료했으니 퀘스트 삭제
    db.session.commit()
    db.session.remove()

    return jsonify({
        "code" : 1,
        "msg" : "보상 수령!",
    })
#================================================================================

@bp.before_request # 이 애너테이션이 적용된 함수는 라우팅 함수보다 항상 먼저 실행
def check_quest_date():
    now = datetime.datetime.now()
    quest_lst = Quest.query.all()
    for q in quest_lst:
        if q.end_date < now:
            db.session.delete(q)
    db.session.commit()
    db.session.remove()

def get_infoList(info_list):
    lst = []
    for info in info_list:
        lst.append(
            {
                "quest_id": info.id,
                "title": info.title,
                "description": info.description,
                "start_date": info.start_date.strftime('%Y-%m-%d'),
                "end_date": info.end_date.strftime('%Y-%m-%d'),
                "user_id": info.user_id,
                "teacher_id": info.teacher_id,
                "done": info.done,
                "check": info.check
            }
        )
    return lst

# def get_info(info):
#     data = {
#         "quest_id" : info.id,
#         "title" : info.title,
#         "description" : info.description,
#         "start_date": info.start_date.strftime('%Y-%m-%d'),
#         "end_date": info.end_date.strftime('%Y-%m-%d'),
#         "done": info.done,
#         "check": info.check
#     }
#     return data