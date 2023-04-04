from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, validators
from wtforms.validators import DataRequired


class Movie_form(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired])
    rating = FloatField("Rating", validators=[DataRequired(), validators.number_range(min=0, max=10)])
    ranking = IntegerField("Ranking", validators=[DataRequired(), validators.number_range(min=0, max=10)])
    review = StringField("Review", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    submit = SubmitField("Submit")