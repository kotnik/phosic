import os
import datetime
import logging
from subprocess import CalledProcessError

from flask_app import make_celery, models, db
from utils import check_call
from sqlalchemy.sql import func

log = logging.getLogger(__name__)

celery = make_celery()

@celery.task()
def calculate_statistics():
    # Load initial values.
    stats = {}
    for stat_name in [ "created", "downloaded", "active", "data_upload" ]:
        stats[stat_name] = models.Stat.query.filter_by(name=stat_name).first()
        if not stats[stat_name]:
            stats[stat_name] = models.Stat(
                name=stat_name,
                value="",
            )
            db.session.add(stats[stat_name])

    # Count created videos.
    s_created = models.Job.query.filter_by(state=((models.JOB_FINISHED) | (models.JOB_DELETED))).count()
    stats['created'].value = "%s" % s_created

    # Sum downloads.
    s_downloaded = db.session.query(func.sum(models.Job.download_count).label("downloaded")).first()
    stats['downloaded'].value = "%s" % s_downloaded

    # Count active videos.
    s_active = models.Job.query.filter_by(state=((models.JOB_PENDING) | (models.JOB_STARTED))).count()
    stats['active'] = s_active

    # Sum data uploaded.
    stats['data_upload'].value = 0
    for job in models.Job.query.filter_by(state=((models.JOB_FINISHED) | (models.JOB_DELETED))).all():
        stats['data_upload'].value = stats['data_upload'].value + job.vid_size * job.download_count

    db.session.commit()
    return True

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

        job.vid_size = os.path.getsize(out)
        job.state = models.JOB_FINISHED
        job.finished = datetime.datetime.utcnow()
        db.session.commit()

    except (CalledProcessError, os.error), e:
        # Encoding failed.
        job.state = models.JOB_FAILED
        db.session.commit()
        log.error("Failed processing %s: %s" % (job_id, e))
        return False

    return True
