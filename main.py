from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import requests
from dotenv import load_dotenv
import os
from form import Movie_form, Edit_movie_form

load_dotenv()
MOVIE_API_KEY = os.getenv("MOVIE_API_KEY")

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
    rating = db.Column(db.Integer, unique=False, nullable=True)
    ranking = db.Column(db.Integer, unique=True, nullable=True)
    review = db.Column(db.String(250), unique=True, nullable=True)
    img_url = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return '<Movie %>' % self.title




@app.route("/")
def home():
    movies_data = db.session.query(Movie).order_by(Movie.rating.asc()).all()
    ranking_value = len(movies_data)
    for movie in movies_data:
        movie.ranking = ranking_value
        db.session.commit()
        ranking_value -= 1
    return render_template("index.html", movies=movies_data)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    movie_form = Movie_form()
    if movie_form.validate_on_submit():
        tmdb_endpoint = "https://api.themoviedb.org/3/search/movie"
        parameters = {
            "api_key": MOVIE_API_KEY,
            "language": "en-US",
            "query": movie_form.title.data
        }
        response = requests.get(url=tmdb_endpoint, params=parameters)
        response.raise_for_status()
        movies_data = response.json()
        all_movies = movies_data['results']
        return render_template("select.html", all_movies=all_movies)    
      
    return render_template("add.html", movie_form=movie_form)


@app.route("/fetch_movie/<movie_id>")
def fetch_movie_detail(movie_id):
    parameters = {
            "api_key": MOVIE_API_KEY,
            "language": "en-US",
        }
    response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params=parameters)
    response.raise_for_status()
    movie_details = response.json()
    print(movie_details)
    new_movie = Movie(
        title = movie_details["original_title"],
        year = movie_details["release_date"].split("-")[0],
        description = movie_details["overview"],
        img_url = f"https://www.themoviedb.org/t/p/original/{movie_details['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("update", movie_id=new_movie.id))

@app.route("/update/<int:movie_id>", methods=["GET", "POST"])
def update(movie_id):
    edit_form = Edit_movie_form()
    movie_to_update = Movie.query.filter_by(id=movie_id).first()
    if edit_form.validate_on_submit():
        movie_to_update.review = edit_form.review.data
        movie_to_update.rating = edit_form.rating.data
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
