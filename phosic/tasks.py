import datetime
import logging
from subprocess import CalledProcessError

from flask_app import make_celery, models, db
from utils import check_call

log = logging.getLogger(__name__)

celery = make_celery()

@celery.task()
def calculate_statistics(x, y):
    return x + y

@celery.task()
def delete_expired():
    return True

@celery.task()
def make_video(job_id, pic, mp3, out):
    job = models.Job.query.filter_by(uniqid=job_id).first()
    if not job:
        return False

    try:
        job.state = models.JOB_STARTED
        db.session.commit()

        check_call([ "/usr/bin/ffmpeg", "-loop", "1",
                     "-i", pic, "-i", mp3,
                     "-shortest", "-c:v", "libx264", "-c:a", "copy",
                     "-tune", "stillimage", out ])

        job.state = models.JOB_FINISHED
        job.finished = datetime.datetime.utcnow()
        db.session.commit()

    except CalledProcessError, e:
        # Encoding failed.
        job.state = models.JOB_FAILED
        db.session.commit()
        log.error("Failed processing %s: %s" % (job_id, e))
        return False

    return True
