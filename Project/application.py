import os
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key_Denis_and_VLAD7879845465465489794546___'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)


def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)