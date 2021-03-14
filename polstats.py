import os

from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, SubmitField
from wtforms.validators import URL, DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
    __tablename__ = "countries"
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
    title = StringField("News article title: ", validators=[DataRequired()])
    rating = IntegerField("News sentiment rating: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/articles", methods=["GET"])
def articles():
    articles = Article.query.all()
    return render_template("articles.html", articles=articles)


@app.route("/add_article", methods=["GET"])
def add_article_get():
    form_add_article = ArticleForm()
    return render_template("add_article.html", form=form_add_article)


@app.route("/add_article", methods=["POST"])
def add_article_post():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        rating = form.rating.data
        new_article = Article(title=title, rating=rating)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for("add_article_get"))
