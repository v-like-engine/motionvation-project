import os
import random
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user

from motionvation.data import db_session
from motionvation.data.models.users import User
from motionvation.forms import RegisterForm
from motionvation.forms.login_form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_Denis_and_VLADiSLav___'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/planger')
def index():
    return render_template('planger.html', title='Your PLANger', text="Stand up and do something!!!")


@app.route('/mynotes')
def notes():
    return render_template('notes.html')


@app.route('/music')
def music():
    return render_template('music_player.html', title='Add your music...', text="Param param pam pam")


@app.route('/')
def main():
    return render_template('main.html', title='Home page')


@app.route('/challenges')
def challenge():
    task = {'few': ['Do chin-ups: ', 'Learn new words in an another language: ', 'Read pages of book: '], 'medium': ['Do push-ups: ', 'Sleep (minutes): ', 'Walk (minutes): '], 'lot': ['Stay home (days): ', 'Eat cookies: ', 'Write code lines: ', 'Read pages of book: '], 'nocount': ['Rearrange things on your table', 'Wash up with cold water', 'Eat a cookie: ', 'Make a note', 'Do the third position thing in your tasktable', 'Draw something funny']}
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
    return render_template('challenges.html', title='Challenges', chs=challenges)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == login_form.email.data).first()
        if not user:
            return render_template('login.html', form=login_form, message="No such user")
        if user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=login_form, message="Wrong password")
    else:
        return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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
    print('кря')
    return render_template('register.html', title='Register', form=form)


@app.route('/nothing')
def nothing():
    return render_template('nothing.html', title='Nothing!')


db_session.global_init('motionvation/db/motionvation.db')
def run():
    # port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080, debug=True)
