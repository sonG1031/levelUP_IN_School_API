from flask import Blueprint, request, jsonify

from api import db
from api.models import SchoolClass

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
        for key, val in data.items():
            sc = SchoolClass.query.filter_by(class_code=key).first()
            sc.port = str(val)
        db.session.commit()
    db.session.remove()
    return jsonify({
        "code" : 1,
    })
