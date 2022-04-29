# quattro_scelte/models/models.py        2022/04/25  M.O
from typing import List, Any
from quattro_scelte import db

class Question(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    inquery = db.Column(db.Text, nullable=True)
    options = db.Column(db.PickleType, nullable=True)
    answer = db.Column(db.Integer, nullable=True)

    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self, inquery: str, options: List[Any], answer: int,
                 create_at, update_at) -> None:
        self.inquery = inquery
        self.options = options
        self.answer = answer
        self.create_at = create_at
        self.update_at = update_at

    def add_question(self) -> None:
        db.session.add(self)
        db.session.commit()


def init():
    db.create_all()

