from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'dev.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS는 SQLAlchemy의 이벤트를 처리하는 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"
JWT_SECRET_KEY = "7x!QG[)'a?9psH?]"
JSON_AS_ASCII = False