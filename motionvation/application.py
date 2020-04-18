import os
import random
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, make_response, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from motionvation.data import db_session
from motionvation.data.models import Note, Category, Task
from motionvation.data.models.users import User
from motionvation.forms import RegisterForm, NotesForm, CategoryForm, TaskForm, ChangePasswordForm, ChangeInfoForm
from motionvation.forms.login_form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_Denis_and_VLADiSLav___'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)
admin_id = 1


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/planger')
@login_required
def index():
    db = db_session.create_session()
    tasks = db.query(Task).filter(Task.user == current_user, Task.priority == 10).all().copy()
    for i in range(9, 0, -1):
        if len(tasks) < 5:
            tasks += db.query(Task).filter(Task.user == current_user, Task.priority == i).all().copy()
    if len(tasks) > 5:
        tasks = tasks[:5]
    return render_template('planger.html', tasks=tasks, title='Your PLANger', text="Your most significant and urgent tasks!", useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/tasks')
@login_required
def tasks():
    db = db_session.create_session()
    tasks = db.query(Task).filter(Task.user == current_user).all().copy()
    new_tasks = []
    priority_now = 10
    while priority_now != -1:
        for task in tasks:
            if task.priority == str(priority_now):
                new_tasks.append(task)
        priority_now -= 1
    return render_template('tasks.html', tasks=new_tasks, useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/mynotes')
@login_required
def notes():
    db = db_session.create_session()
    notes = db.query(Note).filter(Note.user == current_user).all().copy()
    return render_template('notes.html', notes=notes, useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/mynotes/<int:id>')
@login_required
def notes_info(id):
    db = db_session.create_session()
    note = db.query(Note).filter(Note.user == current_user, Note.id == id).first()
    return render_template('notes_info.html', note=note, useracc=(current_user.name + ' ' + current_user.surname))


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
    return render_template('task_info.html', task=task, useracc=(current_user.name + ' ' + current_user.surname))


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
        db.merge(current_user)
        db.commit()
        return redirect('mynotes')
    return render_template('add_note.html', form=notes_form, useracc=(current_user.name + ' ' + current_user.surname))


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
    return render_template('add_category.html', form=category_form, useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/select_category')
@login_required
def select_category():
    db = db_session.create_session()
    categories = db.query(Category).filter(Category.user_id == admin_id).all().copy()
    return render_template('select_category.html', categories=categories, useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/add_task/<id>', methods=['GET', 'POST'])
@login_required
def add_task(id):
    id = int(id)
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
        db.merge(task)
        db.commit()
        return redirect('/tasks')
    return render_template('add_task.html', form=task_form, useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/categories')
@login_required
def categories():
    db = db_session.create_session()
    categories = db.query(Category).filter(Category.user_id == admin_id).all().copy()
    return render_template('categories.html', categories=categories, useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/music')
@login_required
def music():
    return render_template('music_player.html', title='Add your music...', text="Param param pam pam", useracc=(current_user.name + ' ' + current_user.surname))


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
    expr = 20
    expm = 100
    return render_template('account.html', title='My account', useracc=(current_user.name + ' ' + current_user.surname), rank='Not procrastinator', exp=(str(expr) + '/' + str(expm)), expcur=expr, expmax=expm)


@app.route('/challenges')
@login_required
def challenge():
    task = {'few': ['Do tasks: ', 'Add tasks: ', 'Complete challenges: '], 'medium': ['Add tasks with totally priority sum: ', 'Get experience: ', 'Check pages: '], 'lot': ['Stay home (days): ',], 'nocount': ['Reach new level', 'Complete a task with high priority (>8)', 'Delete a note', 'Make a note', 'Add a task with sport category', 'Get 100 experience']}
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
    return render_template('challenge.html', title='Challenges', chs=challenges, useracc=(current_user.name + ' ' + current_user.surname))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == login_form.email.data).first()
        if not user:
            return render_template('login.html', form=login_form, message="No such user")
        if user.check_password(login_form.password.data):
            login_user(user, remember=True)
            return redirect('/')
        else:
            return render_template('login.html', form=login_form, message="Wrong password")
    else:
        return render_template('login.html', form=login_form)


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
    form = ChangeInfoForm()
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
            print(email)
            if not email:
                user_now.email = form.email.data
            else:
                return render_template('change_info.html', form=form, message='This email is already exists')
        db.commit()
        return redirect('/account_info')
    return render_template('change_info.html', form=form)


@app.route('/nothing')
def nothing():
    return render_template('nothing.html', title='Nothing!', useracc='Account')


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
