import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.cofig['SECRET_KEY'] = 'hard to guess secret key'

db = SQLAlchemy(app)

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


class Article(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    url = db.Column(db.String)
    rating = db.Column(db.Integer)
    date = db.Column(db.Date)
    length = db.Column(db.Integer)
    source = db.Column(db.String)
    countries = db.Column(db.String)
    title = db.Column(db.String)

    def __repr__(self):
        return f"{self.title} publicado en  {self.source}"

class ArticleForm(FlaskForm):
    title = StringField('News artcile title: ', validators=[DataRequired()])
    rating = IntegerField('News sentiment rating: ', validators=[DataRequired()])
    source = StringField('News channel: ', validators=[DataRequired()])
    url = StringField('News web link: ', validators=[URL()])
    date = DateField('News web link: ')
    length = IntegerField('Length of the news article in words: ')
    countries = StringField('Countries involved: ')
    submit =SubmitField('Submit')
    
@app.route('/articles', methods=['GET'])
def articles():
    articles = Article.query.all()
    return render_template('articles.html', articles=articles)