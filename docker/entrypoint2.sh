#!/bin/sh

flask db upgrade
flask auth create
flask run --host=0.0.0.0