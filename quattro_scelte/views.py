# quattro_scelte/views/views.py        2022/04/25  M.O
import random
from flask import request, redirect, url_for, render_template, \
    session, Blueprint, current_app, flash
from .models import Question
from .forms import QuizEntryForm, QuizAnswerForm

views = Blueprint('views', __name__)

@views.route('/')
def index():
    session['comp'] = False
    return render_template('index.html')

@views.route('/quiz', methods=['GET', 'POST'])
def quiz():
    question_volume = Question.query.count()
    if question_volume <= 0:
        flash(message='クイズがありません。クイズを登録しましよう！')
        return redirect(url_for('views.quiz_entry'))

    set_id = random.randint(1, question_volume)
    print(set_id)
    question = Question.query.filter_by(id=set_id).first()
    form = QuizAnswerForm(request.form)
    if request.method == 'POST' and form.validate():
        if int(question.answer) == int(form.answer.data):
            session['result'] = True
        else:
            session['result'] = False
        return redirect(url_for('views.quiz_result'))
    return render_template('quiz.html', form=form, question=question)


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
        question = Question(
            inquery=form.inquery.data,
            options=[form.option_1.data, form.option_2.data,
                     form.option_3.data, form.option_4.data],
            answer=form.answer.data
        )
        question.add_question()
        session['comp'] = True
        return redirect(url_for('views.quiz_entry'))
    return render_template('quiz_entry.html', form=form)


@views.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('views.index'))
