from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

from flask_mongoengine import MongoEngine

from config import MONGO_URI, CSR_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = CSR_KEY
csrf = CSRFProtect(app)

app.config['MONGODB_SETTINGS'] = {
    'host': MONGO_URI,
}

db = MongoEngine(app)

class Reviews(db.Document):
    medium = db.StringField(required=True)
    review_title = db.StringField(required=True,unique=True)
    piece_title = db.StringField(required=True)
    artist = db.StringField()
    description = db.StringField(required=True)
    rating = db.IntField(required=True)

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
    reviews = Reviews.objects.all()
    return render_template('reviews.html', reviews=reviews)

@app.route('/create_review', methods=['GET','POST'])
def create_review():

    form = ReviewForm()
    print(request.method)
    if request.method=='POST':
        print('yeah')
        if form.validate_on_submit():
            print('validated')
            review = Reviews(
                medium = form.medium.data,
                review_title = form.review_title.data,
                piece_title = form.piece_title.data,
                artist = form.artist.data,
                description = form.description.data,
                rating = form.rating.data
            )
            review.save()
            print('here')
            return redirect(url_for('submit_review'))
        else:
            print('not validated')
    return render_template('create_review.html', form=form)

@app.route('/submit_review',methods=['GET','POST'])
def submit_review():
    print('rendered')
    form = ReviewForm()
    return render_template('submit_review.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)