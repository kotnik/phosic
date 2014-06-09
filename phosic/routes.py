import os
import datetime

from flask import render_template, redirect, url_for
from werkzeug import secure_filename

from flask_app import app, db, models
from forms import JobForm
from utils import generate_uniqid
import tasks

@app.route('/',  methods=['GET', 'POST'])
def home():
    """Render website's home page."""
    form = JobForm()

    if form.validate_on_submit():
        uniqid = generate_uniqid(10)
        jobdir = app.config['UPLOAD_FOLDER'] + "/" + uniqid + "/"
        os.makedirs(jobdir)

        mp3_filename = secure_filename(form.mp3.data.filename)
        mp3_new_name = jobdir + uniqid + ".mp3"
        form.mp3.data.save(mp3_new_name)
        pic_filename = secure_filename(form.pic.data.filename)
        _, pic_extension = os.path.splitext(pic_filename)
        pic_new_name = jobdir + uniqid + pic_extension
        form.pic.data.save(pic_new_name)
        video_output = jobdir + uniqid + ".mkv"

        task = tasks.make_video.apply_async(
            (uniqid, pic_new_name, mp3_new_name, video_output),
            countdown=app.config['PHOSIC_TASK_DELAY'],
            expires=app.config['PHOSIC_TASK_MAX_EXECUTION_TIME']
        )

        # Create database item
        job = models.Job(
            uniqid=uniqid,
            task_uuid=task.id,
            email=form.email.data,
            created=datetime.datetime.utcnow(),
            expires=datetime.datetime.utcnow() + datetime.timedelta(days=1),
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
    jobdir = app.config['UPLOAD_FOLDER'] + "/" + job_id + "/"

    task = tasks.make_video.AsyncResult(job.task_uuid)
    if task.ready():
        if task.get():
            if os.path.exists(jobdir + job_id + ".mkv"):
                return render_template('job-ready.html', job=job)
        return render_template('job-failed.html', job=job)

    return render_template('job-pending.html', job=job)

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