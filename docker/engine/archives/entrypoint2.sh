#!/bin/sh

flask db upgrade
flask auth create --pswd "${ADMIN_PASS}"
flask run --host=0.0.0.0