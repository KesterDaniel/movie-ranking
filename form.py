from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, validators
from wtforms.validators import DataRequired, URL
from myvalidators import FloatRange


class Movie_form(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Edit_movie_form(FlaskForm):
    review = StringField("Review", validators=[DataRequired()])
    rating = FloatField("Rating", validators=[DataRequired(), FloatRange(min=0, max=10)])
    update = SubmitField("Update")