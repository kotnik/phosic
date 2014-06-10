import os
import datetime
import logging

from flask import render_template, redirect, url_for, send_from_directory, abort
from werkzeug import secure_filename

from flask_app import app, db, models
from forms import JobForm
from utils import generate_uniqid, filesizeformat
import tasks

log = logging.getLogger(__name__)

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
            expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=app.config["PHOSIC_JOB_EXPIRY_MINUTES"]),
            mp3_name=mp3_filename[:255],
            pic_name=pic_filename[:255],
        )
        db.session.add(job)
        db.session.commit()

        return redirect(url_for('jobs', job_id=job.uniqid))

    return render_template('home.html', form=form)

@app.route('/jobs/<job_id>/')
@app.route('/jobs/<job_id>/view')
def jobs(job_id):
    """Render job page."""
    job = models.Job.query.filter_by(uniqid=job_id).first_or_404()
    jobdir = app.config['UPLOAD_FOLDER'] + "/" + job_id + "/"

    task = tasks.make_video.AsyncResult(job.task_uuid)
    if task.ready():
        if task.get():
            if os.path.exists(jobdir + job_id + ".mkv") and job.state != models.JOB_FAILED:
                return render_template('job-ready.html', job=job)
            elif job.state == models.JOB_DELETED:
                return render_template('job-deleted.html', job=job)

        return render_template('job-failed.html', job=job)

    return render_template('job-pending.html', job=job, started=True if job.state == models.JOB_STARTED else False)

@app.route('/jobs/<job_id>/download')
def download_file(job_id):
    if '.' in job_id or job_id.startswith('/'):
        abort(404)

    job = models.Job.query.filter_by(uniqid=job_id).first_or_404()
    if job.state != models.JOB_FINISHED:
        abort(404)

    job.download_count = job.download_count + 1
    db.session.commit()

    video_file = job_id + "/" + job_id + ".mkv"
    return send_from_directory(app.config['UPLOAD_FOLDER'], video_file,
                               attachment_filename="phosic-video.mkv",
                               as_attachment=True, mimetype='video/x-matroska')

@app.route('/about/')
def about():
    """Render about page."""
    stats = {}
    stats['created'] = 0
    stats['downloaded'] = 0
    stats['active'] = 0
    stats['data_upload'] = 0
    for stat in db.session.query(models.Stat):
        stats[stat.name] = stat.value
    stats['data_upload'] = filesizeformat(stats['data_upload'])
    if not stats['active']:
        stats['active'] = "Idle"

    return render_template('about.html', stats=stats)

@app.route('/contact/')
def contact():
    """Render contact page."""
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
