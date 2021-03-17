import os
import datetime 

from flask import Flask, redirect, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, SubmitField
from wtforms.validators import URL, DataRequired, Optional


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "hard to guess secret key"
app.config["EXPLAIN_TEMPLATE_LOADING"] = True

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/")
def index():
    form = ArticleForm()
    return render_template("index.html", form=form)


@app.route("/user/<name>")
def user(name):
    lazy_users = ["ignacio", "xavier", "pablo", "matias", "matías", "gabriel"]
    if name.lower() in lazy_users:
        return render_template("lazy_user.html", name=name)
    else:
        return render_template("user.html", name=name)


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    url = db.Column(db.String)
    rating = db.Column(db.Integer)
    date = db.Column(db.Date, default=datetime.date.today())
    length = db.Column(db.Integer)
    source = db.Column(db.String)
    countries = db.Column(db.String)
    title = db.Column(db.String)

    def __repr__(self):
        return f"{self.title} publicado en  {self.source}"


class ArticleForm(FlaskForm):
    title = StringField("News article title: ", validators=[DataRequired()])
    rating = IntegerField("News sentiment rating: ", validators=[DataRequired()])
    source = StringField("News channel: ", validators=[DataRequired()])
    url = StringField("News web link: ", validators=[URL()])
    date = DateField("Date of the news: ", validators=[Optional()])
    length = IntegerField("Length of the news article in words: ")
    countries = StringField("Countries involved: ")
    submit = SubmitField("Submit")


@app.route("/add_article", methods=['GET'])
def add_article_get():
    form = ArticleForm()
    return render_template("add_article.html", form=form)

@app.route("/add_article", methods=["POST"])
def add_article_post():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        rating = form.rating.data
        source = form.source.data
        url = form.url.data
        date = form.date.data
        length = form.length.data
        countries = form.countries.data
        new_article = Article(title=title, rating=rating, source=source, url=url, date=date, length=length, countries=countries)
        db.session.add(new_article)
        db.session.commit()
        flash('Article added to the data base. Thank you!')
        return redirect(url_for("add_article_get"))

@app.route("/view_articles", methods=["GET"])
def view_articles():
    articles = Article.query.all()
    return render_template("view_articles.html", articles=articles)