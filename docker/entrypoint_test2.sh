#!/bin/sh

python -m pytest --junitxml=/app/reports/result.xml

python -m pytest --html=/app/reports/report.html --self-contained-html