from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import email, DataRequired


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
