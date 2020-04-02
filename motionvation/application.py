import os
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_Denis_and_VLADiSLav___'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

# login_manager = LoginManager()
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#     db = db_session.create_session()
#     return db.query(User).get(user_id)


@app.route('/planger')
def index():
    return render_template('planger.html', title='Your PLANger', text="Stand up and do something!!!")


@app.route('/mynotes')
def note():
    return "my notes!"


@app.route('/music')
def music():
    return render_template('music_player.html', title='Add your music...', text="Param param pam pam")


@app.route('/')
def main():
    return render_template('main.html', title='Home page')


@app.route('/challenges')
def challenge():
    return "Challenge: make a project"


def run():
    # port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=8080, debug=False)