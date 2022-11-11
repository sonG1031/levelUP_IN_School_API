from flask import Blueprint, request, jsonify

from api import db
from api.route.auth import login_required
from api.models import SchoolClass, Game, Inventory, User

bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/port/', methods=['GET', 'POST'])
def port():
    if request.method == 'GET':
        infos = SchoolClass.query.all()
        lst = []
        for info in infos:
            lst.append(info.class_code)
        return jsonify({
            'school_codes' : lst,
        })
    elif request.method == 'POST':
        data = request.get_json()
        if data['type'] == "move":
            del data['type']
            for key, val in data.items():
                sc = SchoolClass.query.filter_by(class_code=key).first()
                sc.move_port = str(val)
            db.session.commit()
        elif data['type'] == "chat":
            del data['type']
            for key, val in data.items():
                sc = SchoolClass.query.filter_by(class_code=key).first()
                sc.chat_port = str(val)
            db.session.commit()
    db.session.remove()
    return jsonify({
        "code" : 1,
    })


@bp.route('/before_connect/', methods=['POST'])
@login_required
def before_connect():
    sc = SchoolClass.query.filter_by(class_code=request.json['class_code']).first()
    if not sc.chat_port or not sc.move_port :
        return jsonify({
            "code" : -1,
            "msg" : "반코드가 존재하지 않습니다.",
            "data" : ""
        })
    return jsonify({
        "code" : 1,
        "msg" : "포트 전송!",
        "data" : [sc.move_port, sc.chat_port]
    })


@bp.route('/level_up/', methods=['POST'])
@login_required
def level_up():
    g = Game.query.filter_by(user_id=request.json['user_id']).first()
    g.level = request.json['level']
    g.exp = request.json['exp']
    g.max_exp = request.json['max_exp']
    g.point = request.json['point']
    db.session.commit()
    db.session.remove()

    return jsonify({
        "code": 1,
        "msg": "레벨업!",
    })


@bp.route('/buy/<string:user_id>', methods=['POST','GET'])
@login_required
def buy(user_id):
    if request.method == "POST":
        g = Game.query.filter_by(user_id=user_id).first()
        g.point = request.json['point']
        inventory = Inventory(
            item_name=request.json['item_name'],
            user_id=user_id
        )
        db.session.add(inventory)
        db.session.commit()
        db.session.remove()
        return jsonify({
            "code": 1,
            "msg": "구매완료!",
        })
    elif request.method == "GET":
        items = Inventory.query.filter_by(user_id=user_id)
        data = ""
        for item in items:
            data = data + f"{item.item_name}," # item1, item2, item3
        return jsonify({
            "code": 1,
            "msg": "인벤토리 반환!",
            "data": data
        })


@bp.route('/ranking/<string:school_code>/<string:class_code>', methods=['GET'])
@login_required
def rank(school_code, class_code):
    school_lst = list(User.query.filter_by(school_code=school_code))
    whole_rank = []
    # class_lst = list(User.query.filter_by(class_code=class_code))
    # class_rank = []

    for sl in school_lst[:]:
        if sl.isStudent == False:
            school_lst.remove(sl)
        sl = {
            "user_id": sl.game_set[0].user_id,
            "exp": sl.game_set.exp,
            "point": sl.game_set.point
        }
        whole_rank.append(sl)

    # for cl in class_lst[:]:
    #     if cl.isStudent == False:
    #         class_lst.remove(cl)
    #     cl = {
    #         "user_id" :  cl.game_set[0].user_id,
    #         "exp" : cl.game_set.exp,
    #         "point" : cl.game_set.point
    #     }
    #     class_rank.append(cl)

    whole_rank = sorted(whole_rank, key=lambda x: (x["exp"], x["point"]), reverse=True)
    # class_rank = sorted(class_rank, key=lambda x: (x["exp"], x["point"]), reverse=True)  # 경험치를 기준으로 순위

    return jsonify({
        "code" : 1,
        "msg" : "랭킹 반환!",
        "whole_rank" : whole_rank,
        # "class_rank" : class_rank
    })

@bp.route('/addExp/<string:user_id>', methods=['POST'])
@login_required
def add_exp(user_id):
    g = Game.query.filter_by(user_id=user_id).first()
    g.exp = request.json['exp']

    db.session.commit()
    db.session.remove()
    return jsonify({
        "code" : 1,
        "msg" : "경험치 저장 완료!"
    })

