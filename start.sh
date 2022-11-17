#!/bin/bash
pipenv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8082