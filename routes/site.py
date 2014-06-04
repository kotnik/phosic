import os

from flask import render_template, redirect, url_for, abort
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug import secure_filename

from wtforms.fields.html5 import EmailField
from wtforms.validators import email, DataRequired

from app import app


class MyForm(Form):
    email = EmailField('Email', validators=[ DataRequired(), email() ])
    mp3 = FileField('MP3', validators=[
            FileRequired(), FileAllowed(['mp3'], 'Please upload MP3 only!')
        ])
    pic = FileField('Picture', validators=[
            FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Please upload images only!')
        ]
    )


@app.route('/',  methods=['GET', 'POST'])
def home():
    """Render website's home page."""
    form = MyForm()

    if form.validate_on_submit():
        mp3filename = secure_filename(form.mp3.data.filename)
        form.mp3.data.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + mp3filename))
        picfilename = secure_filename(form.pic.data.filename)
        form.pic.data.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + picfilename))
        return redirect(url_for('jobs', job_id=1))

    return render_template('home.html', form=form)

@app.route('/jobs/<job_id>')
def jobs(job_id):
    """Render the website's about page."""
    print "Job ID: %s" % job_id
    if job_id != "1":
        abort(404)

    return render_template('job.html')

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
