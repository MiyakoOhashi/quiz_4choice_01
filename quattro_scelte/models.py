# quattro_scelte/models/models.py        2022/04/25  M.O
from typing import List, Any
from flask_bcrypt import generate_password_hash, check_password_hash
from quattro_scelte import db, login_manager
from flask_login import UserMixin
from sqlalchemy import func


class Question(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    inquery = db.Column(db.Text)
    options = db.Column(db.PickleType)
    answer = db.Column(db.Integer)

    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, inquery: str, options: List[Any], answer: int,
                 create_at, update_at, user_id: int) -> None:
        self.inquery = inquery
        self.options = options
        self.answer = answer
        self.create_at = create_at
        self.update_at = update_at
        self.user_id = user_id

    def add_question(self) -> None:
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    def modify_question(self, inquery: str, options: List[Any], answer: int, update_at) -> None:
        with db.session.begin(subtransactions=True):
            self.inquery = inquery
            self.options = options
            self.answer = answer
            self.update_at = update_at
        db.session.commit()

    def delete_question(self):
        with db.session.begin(subtransactions=True):
            db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_max_id(cls):
        res = db.session.query(func.max(cls.id).label('max_id')).one()
        return res.max_id


@login_manager.user_loader
def load_user(user_id) -> List[Any]:
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(128))

    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    questions = db.relationship('Question', backref='users')
    results = db.relationship('Result', backref='users')

    def __init__(self, username, password, create_at, update_at) -> None:
        self.username = username
        self.password = generate_password_hash(password)
        self.create_at = create_at
        self.update_at = update_at

    def validate_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    def add_user(self) -> None:
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_by_username(cls, username) -> List[Any]:
        return cls.query.filter_by(username=username).first()

    def show_questions(self) -> None:
        for question in self.questions:
            print(question.id)

    def delete_user(self):
        with db.session.begin(subtransactions=True):
            db.session.delete(self)
        db.session.commit()


class Result(db.Model):

    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(db.PickleType)
    answers = db.Column(db.PickleType)
    responded_num = db.Column(db.Integer)
    corrected_num = db.Column(db.Integer)

    create_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, questions: List[int], answers: List[int], responded_num: int,
                 corrected_num: int, create_at, user_id: int) -> None:
        self.questions = questions
        self.answers = answers
        self.responded_num = responded_num
        self.corrected_num = corrected_num
        self.create_at = create_at
        self.user_id = user_id

    def add_result(self) -> None:
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def show_result(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


def init():
    db.create_all()

