#!/bin/sh
fecha=$(date +%s)
python3 manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > dump_$fecha.json 