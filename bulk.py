import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atchapedia.settings')
django.setup()

from movies.models import *


f = open('data.csv', 'r', encoding='utf-8')
info = []

rdr = csv.reader(f)
for row in rdr:
    name, email = row
    tuple = (name, email)
    info.append(tuple)
f.close()

instances = []
for (name, email) in info:
    instances.append(User(full_name=name, email=email, status="수강생"))

User.objects.bulk_create(instances)
