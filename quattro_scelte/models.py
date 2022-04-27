# quattro_scelte/models/models.py        2022/04/25  M.O
from typing import List, Any
from quattro_scelte import db

class Question(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    inquery = db.Column(db.Text)
    option_0 = db.Column(db.String(128))
    option_1 = db.Column(db.String(128))
    option_2 = db.Column(db.String(128))
    option_3 = db.Column(db.String(128))
    answer = db.Column(db.Integer)

    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __init__(self, inquery: str, options: List[Any], answer: int) -> None:
        self.inquery = inquery
        self.option_0 = options[0]
        self.option_1 = options[1]
        self.option_2 = options[2]
        self.option_3 = options[3]
        self.answer = answer

    def add_question(self) -> None:
        db.session.add(self)
        db.session.commit()


def init():
    db.create_all()

