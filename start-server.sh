#!/bin/bash
nohup gunicorn core.wsgi:application --workers=2 --bind 0.0.0.0:8000 >> logs/api.out 2>&1 &
daphne -b 0.0.0.0 -p 8001 --proxy-headers core.asgi:application