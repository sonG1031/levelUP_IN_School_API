from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(): # <-- 애플리케이션 팩토리
    app = Flask(__name__)

    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    from .route import auth, game, quest, notice, qr
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)
    app.register_blueprint(quest.bp)
    app.register_blueprint(notice.bp)
    app.register_blueprint(qr.bp)

    return app