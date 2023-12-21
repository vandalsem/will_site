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

@app.route('/review/<review_id>')
def review_details(review_id):
    review = Reviews.objects.get(id=review_id)
    return render_template('review_details.html', review=review)

########
# CRUD #
########

@app.route('/create_review', methods=['GET','POST'])
def create_review():

    form = ReviewForm()
    
    if request.method=='POST' and form.validate_on_submit():

        review = Reviews(
            medium = form.medium.data,
            review_title = form.review_title.data,
            piece_title = form.piece_title.data,
            artist = form.artist.data,
            description = form.description.data,
            rating = form.rating.data
        )

        review.save()
        print(review.id)
        return redirect(url_for('submit_review'))
    
    return render_template('create_review.html', form=form)

@app.route('/edit_review/<review_id>', methods=['GET','POST'])
def edit_review(review_id):
    review = Reviews.objects.get(id=review_id)
    form = ReviewForm(request.form, obj=review)

    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('reviews'))
        if form.validate_on_submit():
            form.populate_obj(review)
            review.save()
            return redirect(url_for('reviews'))

    return render_template('edit_review.html', form=form, review=review)

@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    review = Reviews.objects.get(id=review_id)
    if review:
        review.delete()
    return redirect(url_for('reviews'))

@app.route('/submit_review',methods=['GET','POST'])
def submit_review():
    return render_template('submit_review.html')

if __name__ == '__main__':
    app.run(debug=True)