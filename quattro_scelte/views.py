# quattro_scelte/views/views.py        2022/04/25  M.O
import random
from datetime import datetime
from flask import request, redirect, url_for, render_template, \
    session, Blueprint, current_app, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Question, User, Result
from .forms import QuizEntryForm, QuizAnswerForm, LoginForm, RegisterForm,\
    QuizModifyForm, QuizDeleteForm, UserDeleteForm

views = Blueprint('views', __name__, url_prefix='')

@views.route('/')
def index():
    session['comp'] = False
    return render_template('index.html')


@views.route('/quiz_start', methods=['GET', 'POST'])
def quiz_start():
    question_volume = Question.query.count()
    session['quiz_num'] = 10
    if question_volume < session['quiz_num']:
        flash(message='クイズが足りません。クイズを登録しましよう！')
        return redirect(url_for('views.quiz_entry'))
    session['quiz_count'] = 0
    session['quiz_correct'] = 0
    session['questions'] = []
    session['answers'] = []
    session['previously'] = []
    return render_template('quiz_start.html')


@views.route('/quiz', methods=['GET'])
def quiz_prepare():
    session['quiz_count'] += 1
    while True:
        set_id = random.randint(1, Question.get_max_id())
        if set_id not in session['previously'] and Question.query.get(set_id):
            break
    session['previously'].append(set_id)
    session['questions'].append(set_id)
    return redirect(url_for('views.quiz', set_id=set_id))


@views.route('/quiz/<int:set_id>', methods=['GET', 'POST'])
def quiz(set_id):
    question = Question.query.filter_by(id=set_id).first()
    form = QuizAnswerForm(request.form)
    form.set_labels(question.options)
    if request.method == 'POST' and form.validate():
        session['answers'].append(int(form.answer.data))
        if int(question.answer) == int(form.answer.data):
            session['result'] = True
            session['quiz_correct'] += 1
        else:
            session['result'] = False
        return redirect(url_for('views.quiz_judge'))
    return render_template('quiz.html', form=form, question=question)


@views.route('/quiz_judge', methods=['GET'])
def quiz_judge():
    if session['quiz_count'] >= session['quiz_num']:
        return redirect(url_for('views.quiz_result'))
    return render_template('quiz_judge.html')


@views.route('/quiz_result', methods=['GET'])
def quiz_result():
    results = []
    for q_id, a_id in zip(session['questions'], session['answers']):
        question = Question.query.filter_by(id=q_id).first()
        q = question.inquery
        a = question.options[a_id]
        j = '正解' if question.answer == a_id else '不正解'
        result = (q, a, j)
        results.append(result)
    if current_user.is_authenticated:
        result = Result(
            questions = session['questions'],
            answers = session['answers'],
            responded_num = session['quiz_count'],
            corrected_num = session['quiz_correct'],
            create_at = datetime.now(),
            user_id = current_user.id
        )
        result.add_result()
    return render_template('quiz_result.html', results=results)


@views.route('/quiz_entry', methods=['GET', 'POST'])
@login_required
def quiz_entry():
    if session['comp'] == True:
        flash(message='クイズを登録しました！')
        session['comp'] = False

    form = QuizEntryForm(request.form)
    if request.method == 'POST' and form.validate():
        question = Question(
            inquery=form.inquery.data,
            options=[form.option_1.data, form.option_2.data,
                       form.option_3.data, form.option_4.data],
            answer=form.answer.data,
            create_at=datetime.now(),
            update_at=datetime.now(),
            user_id = current_user.id
        )
        question.add_question()
        session['comp'] = True
        return redirect(url_for('views.quiz_entry'))
    return render_template('quiz_entry.html', form=form)


@views.route('/quiz_modify/<int:user_id>/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz_modify(user_id: int, quiz_id: int):
    question = Question.query.filter_by(id=quiz_id).first()
    if user_id != current_user.id or current_user.id != question.user_id:
        flash(message='編集できません')
        return redirect(url_for('views.index'))
    form = QuizModifyForm(request.form)
    if request.method == 'GET':
        form.set_default(
            inquery=question.inquery,
            options=question.options,
            answer=question.answer
        )
    elif request.method == 'POST' and form.validate():
        question.modify_question(
            inquery=form.inquery.data,
            options=[form.option_1.data, form.option_2.data,
                       form.option_3.data, form.option_4.data],
            answer=form.answer.data,
            update_at=datetime.now()
        )
        flash(message='クイズを編集しました！')
        return redirect(url_for('views.user'))
    return render_template('quiz_modify.html', form=form)


@views.route('/quiz_delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def quiz_delete(user_id: int):
    form = QuizDeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        question = Question.query.get(form.id.data)
        if user_id != current_user.id or current_user.id != question.user_id:
            flash(message='削除できません')
            return redirect(url_for('views.index'))
        question.delete_question()
        return redirect(url_for('views.user'))
    return redirect(url_for('views.user'))


@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash(message='ログアウトしました')
    return redirect(url_for('views.index'))


@views.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_by_username(form.username.data)
        if user and user.validate_password(form.password.data):
            login_user(user)
            flash(message='ログインしました！')
            next = request.args.get('next')
            if not next:
                next = url_for('views.user')
            return redirect(next)
    return render_template('login.html', form=form)


@views.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            password=form.password.data,
            create_at=datetime.now(),
            update_at=datetime.now()
        )
        user.add_user()
        flash('ユーザー登録が完了しました！')
        return redirect(url_for('views.login'))
    return render_template('register.html', form=form)


@views.route('/user')
@login_required
def user():
    regist_quizes = Question.query.filter_by(user_id=current_user.id).all()
    quiz_results = Result.query.filter_by(user_id=current_user.id).all()

    responded_num = 0
    corrected_num = 0
    for result in quiz_results:
        responded_num += result.responded_num
        corrected_num += result.corrected_num
    try:
        all_acc_rate = corrected_num / responded_num * 100
    except(ZeroDivisionError):
        all_acc_rate = None
    return render_template('user.html', regist_quizes=regist_quizes,
        all_acc_rate=all_acc_rate)


@views.route('/user_delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_delete(user_id: int):
    form = UserDeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.get(form.id.data)
        if user_id != current_user.id or current_user.id != user.id:
            flash(message='削除できません')
            return redirect(url_for('views.index'))
        user.delete_user()
        flash(message='ユーザ登録を削除しました')
        return redirect(url_for('views.index'))
    return render_template('user_delete.html', form=form)


@views.route('/quiz_detail/<int:user_id>/<int:quiz_id>')
@login_required
def quiz_detail(user_id: int, quiz_id: int):
    question = Question.query.filter_by(id=quiz_id).first()
    if user_id != current_user.id or current_user.id != question.user_id:
        flash(message='閲覧できません')
        return redirect(url_for('views.index'))
    delete_form = QuizDeleteForm(request.form)
    if not question:
        return redirect(url_for('views.user'))
    return render_template('quiz_detail.html', question=question, delete_form=delete_form)


@views.app_errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('views.index'))
