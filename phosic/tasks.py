import datetime

from flask_app import make_celery, models, db

celery = make_celery()

@celery.task()
def calculate_statistics(x, y):
    return x + y

@celery.task()
def make_video(job_id, pic, mp3, out):
    # ffmpeg -loop 1 -i image.jpg -i audio.mp3 -shortest -c:v libx264 -c:a copy -tune stillimage result.mkv
    job = models.Job.query.filter_by(uniqid=job_id).first()
    if not job:
        return False
    job.finished = datetime.datetime.utcnow()
    db.session.commit()

    return True
