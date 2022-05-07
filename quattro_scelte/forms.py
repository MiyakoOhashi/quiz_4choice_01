from wtforms.form import Form
from wtforms.fields import StringField, TextAreaField, \
    RadioField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms import ValidationError
from typing import List, Any
from quattro_scelte.models import User


class QuizEntryForm(Form):
    inquery = TextAreaField('問題   ', validators=[DataRequired()])
    option_1 = StringField('選択肢１ ', validators=[DataRequired()])
    option_2 = StringField('選択肢２ ', validators=[DataRequired()])
    option_3 = StringField('選択肢３ ', validators=[DataRequired()])
    option_4 = StringField('選択肢４ ', validators=[DataRequired()])
    answer = RadioField('正解No.',
                        choices=[(0, ('1')), (1, ('2')), (2, ('3')), (3, ('4'))],
                        validators=[DataRequired()])
    submit = SubmitField('登録')


class QuizModifyForm(Form):
    id = HiddenField()
    inquery = TextAreaField('問題   ', validators=[DataRequired()])
    option_1 = StringField('選択肢１ ', validators=[DataRequired()])
    option_2 = StringField('選択肢２ ', validators=[DataRequired()])
    option_3 = StringField('選択肢３ ', validators=[DataRequired()])
    option_4 = StringField('選択肢４ ', validators=[DataRequired()])
    answer = RadioField('正解No.',
                        choices=[(0, ('1')), (1, ('2')), (2, ('3')), (3, ('4'))],
                        validators=[DataRequired()])
    submit = SubmitField('更新')

    def set_default(self, inquery: str, options: List[Any], answer: int):
        self.answer.default = answer
        self.process()
        self.inquery.data = inquery
        self.option_1.data = options[0]
        self.option_2.data = options[1]
        self.option_3.data = options[2]
        self.option_4.data = options[3]


class QuizDeleteForm(Form):
    id = HiddenField()
    submit = SubmitField('削除する')


class QuizAnswerForm(Form):
    answer = RadioField('回答群',
                        choices=[(0, ('0')), (1, ('1')), (2, ('2')), (3, ('3'))],
                        validators=[DataRequired()])
    submit = SubmitField('送信')

    def set_labels(self, options):
        self.answer.choices = [(index, option) for index, option in enumerate(options)]


class LoginForm(Form):
    username = StringField(
        'ユーザ名',
        validators=[DataRequired('ユーザ名を入力してください'), Length(6, 20, '6文字以上20文字以下としてください')]
    )
    password = PasswordField('パスワード', validators=[DataRequired('パスワードを入力してください')])
    submit = SubmitField('ログイン')


class RegisterForm(Form):
    username = StringField(
        'ユーザ名',
        validators=[DataRequired('ユーザ名を入力してください'), Length(6, 20, '6文字以上20文字以下としてください')]
    )
    password = PasswordField(
        'パスワード',
        validators=[DataRequired('パスワードを入力してください'), EqualTo('password_confirm', message='パスワードが一致しません')]
    )
    password_confirm = PasswordField('パスワード(確認用) ', validators=[DataRequired()])
    submit = SubmitField('ユーザ登録')

    def validate_username(self, field):
        if User.select_by_username(field.data):
            raise ValidationError('このユーザーネームはすでに使用されています')


