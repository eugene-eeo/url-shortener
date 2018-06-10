#!/usr/bin/env bash

pip install flask flask-MySQLdb validators
pip install requests pytest
mysql -e "use urlshortener; $(cat init.sql)"
