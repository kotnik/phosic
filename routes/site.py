import os

from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename

from app import app

ALLOWED_EXTS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTS

@app.route('/',  methods=['GET', 'POST'])
def home():
    """Render website's home page."""
    if request.method == 'POST':
        print request.files
        mp3File = request.files.get('mp3File', None)
        if mp3File and allowed_file(mp3File.filename):
            filename = secure_filename(mp3File.filename)
            mp3File.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('jobs', job_id=1))
    return render_template('home.html')

@app.route('/jobs/<job_id>')
def jobs(job_id):
    """Render the website's about page."""
    print "Job ID: %s" % job_id
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
