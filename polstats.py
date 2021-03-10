from logging import DEBUG
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    lazy_users = ['ignacio', 'xavier', 'pablo', 'matias', 'matías', 'gabriel']
    if name.lower() in lazy_users:
        return render_template('lazy_user.html', name=name.title())
    else:
        return render_template('user.html', name=name.title())

