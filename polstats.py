from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    lazy_users = ['ignacio', 'xavier', 'pablo', 'matias', 'matías', 'gabriel']
    if name.lower() in lazy_users:
        return render_template('lazy_user.html', name=name)
    else:
        return render_template('user.html', name=name)

