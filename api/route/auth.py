from flask import Blueprint

bp = Blueprint('test', __name__, url_prefix='/') # URL과 함수의 매핑을 관리하기 위해 사용하는 도구(클래스)

@bp.route('/')
def test():
    return 'Hello WORLD!'