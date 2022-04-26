# quattro_scelte/views/views.py        2022/04/25  M.O
from flask import request, redirect, url_for, render_template, \
    session, Blueprint, current_app, flash
# from ..models.models import Question
from ..forms.forms import QuizEntryForm, QuizAnswer

views = Blueprint('views', __name__)

@views.route('/')
def index():
    session['comp'] = False
    return render_template('index.html')

@views.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # question = Question.query.filter_by(id=id).first()
    form = QuizAnswer(request.form)
    if request.method == 'POST' and form.validate():
        print(form.answer.data)
        return redirect(url_for('views.quiz_result'))
    return render_template('quiz.html', form=form, question='TEXT')


@views.route('/quiz_result', methods=['GET'])
def quiz_result():
    return render_template('quiz_result.html')


@views.route('/quiz_entry', methods=['GET', 'POST'])
def quiz_entry():
    if session['comp']:
        flash(message='クイズを登録しました！')
        session.pop('comp', False)

    form = QuizEntryForm(request.form)

    if request.method == 'POST' and form.validate():
        print(form.inquery.data)
        print([form.option_1.data, form.option_2.data, form.option_3.data, form.option_4.data])
        print(form.answer.data)
        # question = Question(
        #     inquery=form.inquery.data,
        #     options=[form.option_1.data, form.option_2.data,
        #              form.option_3.data, form.option_4.data],
        #     answer=form.answer.data
        # )
        # question.add_question()
        session['comp'] = True
        return redirect(url_for('views.quiz_entry'))
    return render_template('quiz_entry.html', form=form)


@views.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('views.index'))