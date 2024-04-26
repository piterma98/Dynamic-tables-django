#!/bin/bash

exec gunicorn "proexe.wsgi:application" \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 60 \
    --limit-request-field_size 65536 \
    --log-level info
