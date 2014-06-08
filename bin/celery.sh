#!/bin/bash

export CONFIG=conf/development.cfg

celery -A phosic.tasks -b "amqp://phosic:phosic@lab//" worker --loglevel=info --beat
