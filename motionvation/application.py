import os
import random
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, make_response, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from motionvation.challenge_generator import generate_challenge
from motionvation.data import db_session
from motionvation.data.models import Note, Category, Task, News, Challenge
from motionvation.data.models.users import User
from motionvation.forms import RegisterForm, NotesForm, CategoryForm, TaskForm, ChangePasswordForm, ChangeInfoForm, \
    ChangeTaskForm, NewsForm, ChangeNewsForm
from motionvation.forms.change_note_form import ChangeNoteForm
from motionvation.forms.login_form import LoginForm

from motionvation.xp import *
from motionvation.exp_calculator import calculatexp, ranculate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_Denis_and_VLADiSLav___'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)
admin_id = 2


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/planger')
@login_required
def index():
    db = db_session.create_session()
    tasks = db.query(Task).filter(Task.user == current_user, Task.is_performed == False).order_by(Task.priority.desc())[:5]
    return render_template('planger.html', tasks=tasks, title='Your PLANger', 
    text="Your most significant and urgent tasks!", 
    useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/tasks')
@login_required
def tasks():
    db = db_session.create_session()
    tasks = db.query(Task).filter(Task.user == current_user, Task.is_performed == False).all().copy()
    new_tasks = []
    priority_now = 10
    while priority_now != -1:
        for task in tasks:
            if task.priority == str(priority_now):
                new_tasks.append(task)
        priority_now -= 1
    return render_template('tasks.html', tasks=new_tasks, t_page_id=0, 
    useracc=(current_user.name + ' ' + current_user.surname), title='Tasks')


@app.route('/done_tasks')
@login_required
def d_tasks():
    db = db_session.create_session()
    done = db.query(Task).filter(Task.user == current_user, Task.is_performed == True).order_by(Task.priority.desc()).all().copy()
    return render_template('tasks.html', tasks=done, t_page_id=1,
    useracc=(current_user.name + ' ' + current_user.surname), title='Tasks')


@app.route('/all_tasks')
@login_required
def all_tasks():
    db = db_session.create_session()
    done = db.query(Task).filter(Task.user == current_user).order_by(Task.is_performed.desc(), Task.priority.desc()).all().copy()
    return render_template('tasks.html', tasks=done, t_page_id=2,  
    useracc=(current_user.name + ' ' + current_user.surname), title='Tasks')


@app.route('/mynotes')
@login_required
def notes():
    db = db_session.create_session()
    notes = db.query(Note).filter(Note.user == current_user).all().copy()
    return render_template('notes.html', notes=notes, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Notes')


@app.route('/mynotes/<int:id>')
@login_required
def notes_info(id):
    db = db_session.create_session()
    note = db.query(Note).filter(Note.user == current_user, Note.id == id).first()
    return render_template('notes_info.html', note=note, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Notes info')


@app.route('/mynotes/delete/<int:id>')
@login_required
def delete_note(id):
    db = db_session.create_session()
    notes = db.query(Note).filter(Note.user == current_user, Note.id == id).first()
    db.delete(notes)
    db.commit()
    return redirect('/mynotes')


@app.route('/tasks/delete/<int:id>')
@login_required
def delete_task(id):
    db = db_session.create_session()
    tasks = db.query(Task).filter(Task.user == current_user, Task.id == id).first()
    db.delete(tasks)
    db.commit()
    return redirect('/tasks')


@app.route('/tasks/<int:id>')
@login_required
def tasks_info(id):
    db = db_session.create_session()
    task = db.query(Task).filter(Task.user == current_user, Task.id == id).first()
    return render_template('task_info.html', task=task, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Task info')


@app.route('/change_task/<id>', methods=['GET', 'POST'])
@login_required
def change_task(id):
    id = int(id)
    db = db_session.create_session()
    task = db.query(Task).filter(Task.id == id).first()
    all_data = {
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
    }
    form = ChangeTaskForm(data=all_data)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        db.commit()
        return redirect('/tasks')
    return render_template('change_task.html', form=form, title='Change task')


@app.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    notes_form = NotesForm()
    if notes_form.validate_on_submit():
        db = db_session.create_session()
        note = Note()
        note.title = notes_form.title.data
        note.text = notes_form.text.data
        current_user.notes.append(note)
        current_user.xp += adding_note_xp
        db.merge(current_user)
        db.commit()
        return redirect('mynotes')
    return render_template('add_note.html', form=notes_form, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Add note')


@app.route('/change_note/<id>', methods=['GET', 'POST'])
@login_required
def change_note(id):
    id = int(id)
    db = db_session.create_session()
    note = db.query(Note).filter(Note.id == id).first()
    all_data = {
        'title': note.title,
        'text': note.text
    }
    form = ChangeNoteForm(data=all_data)
    if form.validate_on_submit():
        note.title = form.title.data
        note.text = form.text.data
        db.commit()
        return redirect('/mynotes')
    return render_template('change_note.html', form=form, title='Change note')


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.id != admin_id:
        return redirect('/')
    category_form = CategoryForm()
    if category_form.validate_on_submit():
        db = db_session.create_session()
        category = Category()
        category.title = category_form.title.data
        current_user.categories.append(category)
        db.merge(current_user)
        db.commit()
        return redirect('/categories')
    return render_template('add_category.html', form=category_form, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Add category')


@app.route('/select_category')
@login_required
def select_category():
    db = db_session.create_session()
    categories = db.query(Category).filter(Category.user_id == admin_id).all().copy()
    return render_template('select_category.html', categories=categories, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Select category')


@app.route('/add_task/<int:id>', methods=['GET', 'POST'])
@login_required
def add_task(id):
    task_form = TaskForm()
    if task_form.validate_on_submit():
        db = db_session.create_session()
        task = Task()
        task.title = task_form.title.data
        task.description = task_form.description.data
        task.priority = task_form.priority.data
        current_category = db.query(Category).filter(Category.user_id == admin_id, Category.id == id).first()
        task.category = current_category
        task.user = current_user
        current_user.xp += adding_task_xp
        db.merge(task)
        db.commit()
        return redirect('/tasks')
    return render_template('add_task.html', form=task_form, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Add task')


@app.route('/change_task_category/<id>')
@login_required
def change_task_category(id):
    id = int(id)
    db = db_session.create_session()
    categories = db.query(Category).all()
    return render_template('change_task_category.html', title='Change category', task_id=id, categories=categories)


@app.route('/change_task_category/save/<category_id>/<task_id>', methods=['GET', 'POST'])
@login_required
def change_task_category_save(category_id, task_id):
    category_id = int(category_id)
    task_id = int(task_id)
    db = db_session.create_session()
    task = db.query(Task).filter(Task.id == task_id).first()
    task.category_id = category_id
    db.merge(task)
    db.commit()
    return redirect('/tasks')


@app.route('/done_task/<id>')
@login_required
def done_task(id):
    id = int(id)
    db = db_session.create_session()
    task = db.query(Task).filter(Task.user == current_user, Task.id == id).first()
    task.is_performed = True
    user_now = db.query(User).filter(User.id == current_user.id).first()
    user_now.xp += done_task_xp
    db.commit()
    return redirect('/tasks')


@app.route('/undone_task/<id>')
@login_required
def undone_task(id):
    id = int(id)
    db = db_session.create_session()
    task = db.query(Task).filter(Task.user == current_user, Task.id == id).first()
    task.is_performed = False
    db.commit()
    return redirect('/tasks')


@app.route('/categories')
@login_required
def categories():
    db = db_session.create_session()
    categories = db.query(Category).filter(Category.user_id == admin_id).all().copy()
    return render_template('categories.html', categories=categories, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Categories')


@app.route('/music')
@login_required
def music():
    return render_template('music_player.html', title='Add your music...',
                           useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/')
def main():
    if current_user.is_authenticated:
        info = (current_user.name + ' ' + current_user.surname)
    else:
        info = 'Anonymous'
    return render_template('main.html', title='Home page', useracc=info)


@app.route('/account_info')
@login_required
def account_main():
    lvl, maxp, currexp = calculatexp(current_user.xp)
    rank = ranculate(current_user.xp)
    return render_template('account.html', title='My account', user=current_user,
                           useracc=(current_user.name + ' ' + current_user.surname), rank=rank,
                           percentxp=int(currexp * 100 / maxp), currexp=currexp, maxp=maxp, lvl=lvl)


@app.route('/challenges')
@login_required
def challenge():
    task = {'few': ['Do tasks: ', 'Add tasks: ', 'Complete challenges: '],
            'medium': ['Add tasks with totally priority sum: ', 'Get experience: ', 'Check pages: '], 'lot': ['Stay home (days): ',], 'nocount': ['Reach new level', 'Complete a task with high priority (>8)', 'Delete a note', 'Make a note', 'Add a task with sport category', 'Get 100 experience']}
    challenges = []
    for i in range(random.randint(1, 10)):
        t = random.choice(list(task.keys()))
        if t == 'nocount':
            c = ''
        elif t == 'few':
            c = random.randint(1, 10)
        elif t == 'medium':
            c = random.randint(5, 50)
        else:
            c = random.randint(20, 100)
        challenges.append(random.choice(task[t]) + str(c))
    return render_template('challenge.html', title='Challenges', chs=challenges,
                           useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/refresh_challenges', methods=['GET', 'POST'])
@login_required
def refresh():
    db = db_session.create_session()
    challenges_to_del = db.query(Challenge).filter(Challenge.user == current_user, Challenge.is_won == False).all()
    db.delete(challenges_to_del)
    for i in range(5):
        challenge_dict = generate_challenge()
        chall = Challenge()
        chall.title = challenge_dict['text']
        chall.current = 0
        chall.required = challenge_dict['required']
        chall.add_task = 1 in challenge_dict['plot']
        chall.add_note = 2 in challenge_dict['plot']
        chall.delete_task = 3 in challenge_dict['plot']
        chall.delete_note = 4 in challenge_dict['plot']
        chall.do_task = 5 in challenge_dict['plot']
        chall.do_challenge = 6 in challenge_dict['plot']
        chall.get_level = 7 in challenge_dict['plot']
        chall.get_xp = 8 in challenge_dict['plot']
        chall.difficulty = challenge_dict['difficulty']
        current_user.challenges.append(chall)
        db.merge(current_user)
        db.commit()
    return render_template('add_news.html', useracc=(current_user.name + ' ' + current_user.surname),
                           title='Add news')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == login_form.email.data).first()
        if not user:
            return render_template('login.html', form=login_form, message="No such user", title='Login')
        if user.check_password(login_form.password.data):
            login_user(user, remember=True)
            return redirect('/')
        else:
            return render_template('login.html', form=login_form, message="Wrong password", title='Login')
    else:
        return render_template('login.html', form=login_form, title='Login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="Passwords doesn`t match")
        db = db_session.create_session()
        if db.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register',
                                   form=form,
                                   message="User already exists")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            country=form.country.data,
            city=form.city.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.add(user)
        db.commit()
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/change_info', methods=['GET', 'POST'])
@login_required
def change_info():
    all_data = {
        'name': current_user.name,
        'surname': current_user.surname,
        'country': current_user.country,
        'city': current_user.city,
        'email': current_user.email
    }
    form = ChangeInfoForm(data=all_data)
    if form.validate_on_submit():
        db = db_session.create_session()
        user_now = db.query(User).filter(User.id == current_user.id).first()
        if form.name.data:
            user_now.name = form.name.data
        if form.surname.data:
            user_now.surname = form.surname.data
        if form.country.data:
            user_now.country = form.country.data
        if form.city.data:
            user_now.city = form.city.data
        if form.email.data:
            email = db.query(User).filter(User.email == form.email.data).first()
            if not email or user_now == email:
                user_now.email = form.email.data
            else:
                return render_template('change_info.html', form=form, message='This email already exists',
                                       title='Change info')
        db.commit()
        return redirect('/account_info')
    return render_template('change_info.html', form=form, title='Change info')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        user_now = db.query(User).filter(User.id == current_user.id).first()
        if not user_now.check_password(form.old_password.data):
            return render_template('change_password.html', form=form, message='Old password is incorrect',
                                   title='Change password')
        if form.new_password.data != form.new_password_again.data:
            return render_template('change_password.html', form=form, message='Passwords do not match',
                                   title='Change password')
        user_now.set_password(form.new_password.data)
        db.commit()
        return redirect('/account_info')
    return render_template('change_password.html', form=form, title='Change password')


@app.route('/news')
@login_required
def news_main():
    db = db_session.create_session()
    news = db.query(News).filter(News.user_id == admin_id).all().copy()[::-1]
    return render_template('news.html', title='News', news=news, t_page_id=0,
                           useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/all_news')
@login_required
def a_news_main():
    db = db_session.create_session()
    news = db.query(News).all().copy()[::-1]
    return render_template('news.html', title='All news', news=news, t_page_id=2,
                           useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/informal_news')
@login_required
def informal_news():
    db = db_session.create_session()
    news = db.query(News).filter(News.user_id != admin_id).all().copy()[::-1]
    return render_template('news.html', title='Informal news', news=news, t_page_id=1,
                           useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/my_news')
@login_required
def my_news():
    db = db_session.create_session()
    news = db.query(News).filter(News.user == current_user).all().copy()[::-1]
    return render_template('news.html', title='My news', news=news, t_page_id=3,
                           useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        current_user.news.append(news)
        db.merge(current_user)
        db.commit()
        return redirect('/news')
    return render_template('add_news.html', form=form, useracc=(current_user.name + ' ' + current_user.surname),
                           title='Add news')


@app.route('/news_info/<id>')
@login_required
def news_info(id):
    id = int(id)
    db = db_session.create_session()
    news = db.query(News).filter(News.id == id).first()
    return render_template('news_info.html', current_user=current_user, news=news, useracc=(current_user.name + ' ' + current_user.surname),
                           title='News info')


@app.route('/news/delete/<int:id>')
@login_required
def delete_news(id):
    db = db_session.create_session()
    news = db.query(News).filter(News.user == current_user, News.id == id).first()
    db.delete(news)
    db.commit()
    return redirect('/news')


@app.route('/change_news/<id>', methods=['GET', 'POST'])
@login_required
def change_news(id):
    id = int(id)
    db = db_session.create_session()
    news = db.query(News).filter(News.id == id).first()
    all_data = {
        'title': news.title,
        'text': news.text
    }
    form = ChangeNewsForm(data=all_data)
    if form.validate_on_submit():
        news.title = form.title.data
        news.text = form.text.data
        db.commit()
        return redirect('/news')
    return render_template('change_news.html', form=form, title='Change news')


@app.route('/hide_email/<hide_or_show>', methods=['GET', 'POST'])
@login_required
def hide_email(hide_or_show):
    db = db_session.create_session()
    user_now = db.query(User).filter(User.id == current_user.id).first()
    if hide_or_show == 'hide':
        user_now.hide_email = True
    else:
        user_now.hide_email = False
    db.commit()
    return redirect('/account_info')


@app.route('/nothing')
def nothing():
    return render_template('nothing.html', title='Nothing!', useracc='Account')


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', current_user=current_user, useracc=(current_user.name + ' ' + current_user.surname))


@app.errorhandler(404)
def not_found(error):
    if current_user.is_authenticated:
        info = (current_user.name + ' ' + current_user.surname)
    else:
        info = 'Anonymous'
    er_txt = '404 not found: Wrong request: no such web-address!'
    return render_template('error.html', title='Error',
    text=er_txt, useracc=info)


@app.errorhandler(401)
def unauth(error):
    er_txt = '401 not authorized: Please log in or register!!!'
    return render_template('error.html', title='Error',
    text=er_txt)


from os import path
db_session.global_init(path.join(path.dirname(__file__), './db/motionvation.db'))

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
