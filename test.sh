#!/usr/bin/env bash

export URLSHORTENER_DB='urlshortener_testing'
mysql -e "use urlshortener_testing; $(cat init.sql)"
py.test
mysql -e 'use urlshortener_testing; drop table url_tags; drop table url;'
