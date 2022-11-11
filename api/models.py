from api import db


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_code = db.Column(db.String(200), unique=True, nullable=False)
    school_name = db.Column(db.String(200), nullable=False)
    school_time = db.Column(db.Time(), nullable=False)


class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_code = db.Column(db.String(200), db.ForeignKey('school.school_code', ondelete='CASCADE'), nullable=False) # School모델의 id값
    class_code = db.Column(db.String(200), unique=True, nullable=False)
    class_name = db.Column(db.String(200), nullable=False) # quest 통신때문에
    school = db.relationship('School', backref=db.backref('class_set', cascade='all, delete-orphan')) # School모델 참조
    move_port = db.Column(db.String(200), nullable=True) # 멀티룸을 구현하기 위해!, 게임 위치 동기화 목적
    chat_port = db.Column(db.String(200), nullable=True) # 멀티룸을 구현하기 위해! 채팅 목적



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable =False)
    isStudent = db.Column(db.Boolean, nullable=False) # 학생이냐 선생님이냐
    school_code = db.Column(db.String(200), db.ForeignKey('school.school_code', ondelete='CASCADE'), nullable=False)
    school = db.relationship('School', backref=db.backref('user_set', cascade='all, delete-orphan'))
    class_code = db.Column(db.String(200), db.ForeignKey('school_class.class_code', ondelete='CASCADE'),  nullable=False)
    school_class = db.relationship('SchoolClass', backref=db.backref('user_set', cascade='all, delete-orphan'))
    qr = db.Column(db.String(200), nullable=True, unique=True)
    qr_date = db.Column(db.DateTime(), nullable=True)
    qr_checked = db.Column(db.Boolean, server_default='', nullable=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    user = db.relationship('User', backref=db.backref('game_set', cascade='all, delete-orphan'))
    level = db.Column(db.Integer, server_default='1', nullable=True)
    exp = db.Column(db.Integer, server_default='0', nullable=True)
    max_exp = db.Column(db.Integer, server_default='100', nullable=True)
    point = db.Column(db.Integer, server_default='0', nullable=True)


class UserQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    exp = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.String(200), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.String(200), nullable=False) # 자기가 만든 퀘스트가 뭔지 알기 위해서
    user = db.relationship('User', backref=db.backref('Quest_set', cascade='all, delete-orphan'))
    done = db.Column(db.Boolean, server_default='', nullable=True)
    check = db.Column(db.Boolean, server_default='', nullable=True)
    questlst_id = db.Column(db.Integer, db.ForeignKey('quest_list.id', ondelete='CASCADE'), nullable=False)
    questlst = db.relationship('QuestList', backref=db.backref('QuestList_set', cascade='all, delete-orphan'))


class QuestList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    exp = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    class_code = db.Column(db.String(200), nullable=False)
    teacher_id = db.Column(db.String(200), nullable=False) # 자기가 만든 퀘스트가 뭔지 알기 위해서


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=True)
    class_code = db.Column(db.String(200), nullable=False)
    current_date = db.Column(db.DateTime(), nullable=False)
    teacher_id = db.Column(db.String(200), nullable=False)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.String(200), db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('inventory_set', cascade='all, delete-orphan'))
