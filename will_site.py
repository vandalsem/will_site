from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional

from flask_mongoengine import MongoEngine, Document
from mongoengine import StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField

from config import MONGO_USER, MONGO_PASS, MONGO_URI, CSR_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = CSR_KEY
csrf = CSRFProtect(app)

app.config['MONGODB_SETTINGS'] = {
    'host': MONGO_URI,
    'username': MONGO_USER,
    'password': MONGO_PASS,
}

db = MongoEngine(app)

class Review(db.Document):
    medium = db.StringField()
    review_title = db.StringField()
    piece_title = db.StringField()
    artist = db.StringField()
    description = db.StringField()
    rating = db.IntField()

class ReviewForm(FlaskForm):
    medium = StringField('Medium',validators=[DataRequired()])
    review_title = StringField('Review Title',validators=[DataRequired()])
    piece_title = StringField('Piece Title',validators=[DataRequired()])
    artist = StringField('Artist')
    description = TextAreaField('Description',validators=[DataRequired()])
    rating = IntegerField('Rating',validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reviews')
def reviews():
    reviews = Review.objects()
    return render_template('reviews.html', reviews=reviews)

@app.route('/create_review', methods=['GET','POST'])
def create_review():

    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            medium = form.medium.data,
            review_title = form.review_title.data,
            piece_title = form.piece_title.data,
            artist = form.artist.data,
            description = form.description.data,
            rating = form.rating.data
        )
        review.save()
        return redirect(url_for('reviews'))
    return render_template('create_review.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)