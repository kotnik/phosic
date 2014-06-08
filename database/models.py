from flask_app import db

JOB_PENDING = 0
JOB_STARTED = 1
JOB_FINISHED = 2
JOB_DELETED = 3


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_uuid = db.Column(db.String(36), index=True, unique=True)
    created = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
    expires = db.Column(db.DateTime)
    uniqid = db.Column(db.String(10), index=True, unique=True)
    email = db.Column(db.String(120))
    mp3_name = db.Column(db.String(255), default="")
    pic_name = db.Column(db.String(255), default="")
    vid_name = db.Column(db.String(255), default="")
    finished = db.Column(db.SmallInteger, default=JOB_PENDING)

    def __repr__(self):
        return '<Job %r>' % (self.uniqid)
