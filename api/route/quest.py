from flask import Blueprint, request,jsonify
from sqlalchemy import and_

from api import db

from api.models import UserQuest, User, Game, QuestList
from api.route.auth import login_required
import datetime

bp = Blueprint('quest', __name__, url_prefix='/quest')


@bp.route("/app/<string:teacher_id>", methods=["GET", "POST"])
# @login_required
def app_quest(teacher_id): # 자신이 생성한 퀘스트 보기(GET), 퀘스트 추가하기(POST)
    user = User.query.filter_by(user_id = teacher_id).first()
    if user.isStudent == False:
        if request.method == 'POST':
            title = request.json['title']
            description = request.json['description']
            exp = request.json['exp']
            start_date = datetime.datetime.strptime(request.json['start_date'],'%Y-%m-%d')
            end_date = datetime.datetime.strptime(request.json['end_date'],'%Y-%m-%d')
            point = request.json['point']
            class_code = request.json['class_code']

            user_lst = list(User.query.filter(and_(User.class_code == class_code, User.isStudent == True)))
            print(list(user_lst))
            if not user_lst:
                return jsonify({
                    "code": -1,
                    "msg": "반코드가 존재하지 않거나 학생이 없습니다..",
                })
            else:
                q = QuestList(
                    title=title,
                    description=description,
                    exp=exp,
                    start_date=start_date,
                    end_date=end_date,
                    point=point,
                    teacher_id=teacher_id
                )
                db.session.add(q)
                db.session.commit()

                for user in user_lst:
                    data = UserQuest(
                        title = title,
                        description = description,
                        exp = exp,
                        start_date = start_date,
                        end_date = end_date,
                        point = point,
                        user_id = user.user_id,
                        teacher_id = teacher_id,
                        questlst_id=q.id
                    )
                    db.session.add(data)
                db.session.commit()
            db.session.remove()

            return jsonify({
                "code": 1,
                "msg": "퀘스트 추가 성공!",
            })
        elif request.method == 'GET':

            quest_lst = QuestList.query.filter_by(teacher_id=teacher_id) # 내가 만든 퀘스트 목록
            quest_lst = serializable_questList(quest_lst)
            user_quest = UserQuest.query.filter_by(teacher_id=teacher_id)
            user_quest = serializable_userQuest(user_quest)

            db.session.remove()

            return jsonify({
                "code": 1,
                "msg": "퀘스트 목록 반환!",
                "data": {
                    "questList": quest_lst,
                    "userQuest": user_quest
                }
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
    if user.isStudent == False:
        q = UserQuest.query.filter(and_(UserQuest.user_id == request.json['user_id'], UserQuest.id == request.json['id'])).first()
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
        user_quest = UserQuest.query.filter(and_(UserQuest.user_id == user_id, UserQuest.start_date <= now <= UserQuest.end_date))
        user_quest = serializable_userQuest(user_quest)
        db.session.remove()
        return jsonify({
            "code": 1,
            "msg": "유저 퀘스트 목록 반환!",
            "data": user_quest
        })
    elif request.method == "POST": # 퀘스트 완료 요청
        user_quest = UserQuest.query.filter(and_(UserQuest.user_id == user_id, UserQuest.id == request.json['id'])).first()
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
    reward_info = UserQuest.query.filter((UserQuest.user_id == request.json['user_id']) | (UserQuest.id == request.json['id'])).first()
    if reward_info is None:
        return jsonify({
            "code": -1,
            "msg": "요청 오류",
        })
    elif reward_info.check == True:
        game_info.point += reward_info.point
        game_info.exp += reward_info.exp
    else:
        return jsonify({
            "code" : -1,
            "msg" : "요청 오류",
        })
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
    quest_lst = QuestList.query.all()
    for q in quest_lst:
        if q.end_date < now:
            db.session.delete(q)
    db.session.commit()
    db.session.remove()


def serializable_userQuest(info_list):
    lst = []
    for info in info_list:
        lst.append(
            {
                "id": info.id,
                "title": info.title,
                "description": info.description,
                "start_date": info.start_date.strftime('%Y-%m-%d'),
                "end_date": info.end_date.strftime('%Y-%m-%d'),
                "user_id": info.user_id,
                "teacher_id": info.teacher_id,
                "exp":info.exp,
                "point":info.point,
                "done": info.done,
                "check": info.check,
                "questlst_id":info.questlst_id
            }
        )
    return lst

def serializable_questList(info_list):
    lst = []
    for info in info_list:
        lst.append(
            {
                "id": info.id,
                "title": info.title,
                "description": info.description,
                "start_date": info.start_date.strftime('%Y-%m-%d'),
                "end_date": info.end_date.strftime('%Y-%m-%d'),
                "exp":info.exp,
                "point":info.point,
                "teacher_id": info.teacher_id,
            }
        )
    return lst