#!/usr/bin/env bash
coverage run --omit=*/venv/*,*/migrations/*,manage.py manage.py test && coverage report
