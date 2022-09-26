from api import db


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_code = db.Column(db.String(200), unique=True, nullable=False)
    school_name = db.Column(db.String(200), nullable=False)


class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_code = db.Column(db.String(200), db.ForeignKey('school.school_code', ondelete='CASCADE'), nullable=False) # School모델의 id값
    class_code = db.Column(db.String(200), unique=True, nullable=False)
    school = db.relationship('School', backref=db.backref('class_set', cascade='all, delete-orphan')) # School모델 참조


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable =False)
    job = db.Column(db.String(200), nullable=False) # 학생이냐 선생님이냐
    school_code = db.Column(db.String(200), db.ForeignKey('school.school_code', ondelete='CASCADE'), nullable=False)
    school = db.relationship('School', backref=db.backref('user_set', cascade='all, delete-orphan'))
    class_code = db.Column(db.String(200), db.ForeignKey('school_class.class_code', ondelete='CASCADE'),  nullable=True)
    school_class = db.relationship('SchoolClass', backref=db.backref('user_set', cascade='all, delete-orphan'))
    qr = db.Column(db.String(200), nullable=True, unique=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    top = db.Column(db.String(200), nullable=False)
    bottom = db.Column(db.String(200), nullable=False)
    hair = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(200), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    # username = db.Column(db.String(200), db.ForeignKey('user.username', ondelete='CASCADE'), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    user = db.relationship('User', backref=db.backref('game_set', cascade='all, delete-orphan'))
    level = db.Column(db.Float, nullable=False)
    point = db.Column(db.Integer, nullable=False)


class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    exp = db.Column(db.Float, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    period = db.Column(db.DateTime(), nullable=False)
    class_code = db.Column(db.String(200), db.ForeignKey('school_class.class_code', ondelete='CASCADE'), nullable =False)
    # school_class = db.relationship('SchoolClass', backref=db.backref('user_set', cascade='all, delete-orphan')) # 충돌이슈때문에, 그리고 불필요한것같아서

