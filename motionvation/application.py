import os
import random
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user

from motionvation.data import db_session
from motionvation.data.models.users import User
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
    task = ['Do push-ups: ', 'Sleep (minutes): ']
    challenges = []
    for i in range(random.randint(1, 10)):
        challenges.append(random.choice(task) + str(random.randint(5, 50)))
    return render_template('challenges.html', title='Challenges', chs=challenges)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == login_form.email.data).first()
        if not user:
            return render_template('login.html', form=login_form, message="Такого пользователя не существует")
        if user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', form=login_form, message="Неверный пароль")
    else:
        return render_template('login.html', form=login_form)


@app.route('/nothing')
def nothing():
    return render_template('nothing.html', title='Nothing!')


def run():
    # port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080)