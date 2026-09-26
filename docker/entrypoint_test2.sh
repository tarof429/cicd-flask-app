#!/bin/sh

python -m pytest -v --junitxml=/app/reports/result.xml

python -m pytest -v  --html=/app/reports/report.html --self-contained-html