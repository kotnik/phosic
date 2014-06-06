import os
import random
import string
import datetime

from flask import render_template, redirect, url_for
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug import secure_filename

from wtforms.fields.html5 import EmailField
from wtforms.validators import email, DataRequired

from app import app, db, models


class JobForm(Form):
    email = EmailField('Email', validators=[ DataRequired(), email() ])
    mp3 = FileField('MP3', validators=[
            FileRequired(), FileAllowed(['mp3'], 'Please upload MP3 only!')
        ])
    pic = FileField('Picture', validators=[
            FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Please upload images only!')
        ]
    )
    recaptcha = RecaptchaField()


def generate_uniqid(length):
    return ''.join(
        random.choice(string.lowercase+string.digits) for i in range(length)
    )

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/',  methods=['GET', 'POST'])
def home():
    """Render website's home page."""
    form = JobForm()

    if form.validate_on_submit():
        uniqid = generate_uniqid(10)
        jobdir = app.config['UPLOAD_FOLDER'] + "/" + uniqid + "/"
        os.makedirs(jobdir)

        mp3_filename = secure_filename(form.mp3.data.filename)
        form.mp3.data.save(jobdir + uniqid + ".mp3")
        pic_filename = secure_filename(form.pic.data.filename)
        _, pic_extension = os.path.splitext(pic_filename)
        form.pic.data.save(jobdir + uniqid + pic_extension)

        # TODO: Send job to processing

        # Create database item
        job = models.Job(
            uniqid=uniqid,
            email=form.email.data,
            created=datetime.datetime.utcnow(),
            mp3_name=mp3_filename[:255],
            pic_name=pic_filename[:255],
        )
        db.session.add(job)
        db.session.commit()

        return redirect(url_for('jobs', job_id=job.uniqid))

    return render_template('home.html', form=form)

@app.route('/jobs/<job_id>')
def jobs(job_id):
    """Render the website's about page."""
    job = models.Job.query.filter_by(uniqid=job_id).first_or_404()
    return render_template('job.html', job=job)

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/contact/')
def contact():
    """Render website's home page."""
    return render_template('contact.html')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)
