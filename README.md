Phosic
======

Simple web service to join mp3 file and a picture using Flask, ffmpeg, Celery,
SQLite and Redis.

How to run it?
--------------

In development mode, create virtual environment and install `requirements.txt`
with pip, and then create the database:

    ./db_create.py
    ./db_upgrade.py

After that just use the script in `bin` folder to run it:

    ./bin/run.sh

Now you can access the website at http://localhost:8000

Production
----------

To run phosic in production see `conf` directory for nginx configuration and
supervisord units.
