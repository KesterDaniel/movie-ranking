from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import requests
from form import Movie_form, Edit_movie_form

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(app)
app.app_context().push()
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    ranking = db.Column(db.Integer, unique=True, nullable=False)
    review = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return '<Movie %>' % self.title




@app.route("/")
def home():
    movies_data = db.session.query(Movie).all()
    sorted_movies_data = sorted(movies_data, key=lambda x: x.ranking)    
    return render_template("index.html", movies=sorted_movies_data)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    movie_form = Movie_form()
    if movie_form.validate_on_submit():
        try:
            new_movie = Movie(
                title = movie_form.title.data,
                year = movie_form.year.data,
                description = movie_form.description.data,
                rating = movie_form.rating.data,
                ranking = movie_form.ranking.data,
                review = movie_form.review.data,
                img_url = movie_form.img_url.data
            )
            db.session.add(new_movie)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "Some entries have been saved before. Please add different values"
        else:
            return redirect(url_for("add_movie"))
    return render_template("add.html", movie_form=movie_form)


@app.route("/update/<int:movie_id>", methods=["GET", "POST"])
def update(movie_id):
    edit_form = Edit_movie_form()
    movie_to_update = Movie.query.filter_by(id=movie_id).first()
    if edit_form.validate_on_submit():
        movie_to_update.review = edit_form.review.data
        movie_to_update.ranking = edit_form.ranking.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", edit_form=edit_form, movie=movie_to_update)


@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
