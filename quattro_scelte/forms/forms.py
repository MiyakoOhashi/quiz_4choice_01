from wtforms.form import Form
from wtforms.fields import StringField, TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired
StringField()
class QuizEntryForm(Form):
    inquery = TextAreaField('問題   ', validators=[DataRequired()])
    option_1 = StringField('選択肢1 ', validators=[DataRequired()])
    option_2 = StringField('選択肢2 ', validators=[DataRequired()])
    option_3 = StringField('選択肢3 ', validators=[DataRequired()])
    option_4 = StringField('選択肢4 ', validators=[DataRequired()])
    answer = RadioField('正解No',
                        choices=[(0, ('1')), (1, ('2')), (2, ('3')), (3, ('4'))],
                        validators=[DataRequired()])
    submit = SubmitField('登録')


class QuizAnswer(Form):
    answer = RadioField('回答',
                        choices=[(0, ('1')), (1, ('2')), (2, ('3')), (3, ('4'))],
                        validators=[DataRequired()])
    submit = SubmitField('送信')