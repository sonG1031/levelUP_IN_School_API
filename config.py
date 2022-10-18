import os

BASE_DIR = os.path.dirname(__file__)
# SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'dev.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS는 SQLAlchemy의 이벤트를 처리하는 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = "7x!QG[)'a?9psH?]"