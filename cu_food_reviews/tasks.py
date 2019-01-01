from __future__ import absolute_import, unicode_literals
from django.core.management import call_command
from .celery import app

@app.task
def load_data_from_endpoint_task():
    call_command('load_data_from_endpoint')

@app.task
def add(x, y):
    print("adding {} and {} together".format(x,y))
    return x + y

@app.task
def fib(n):
    if n <= 1: return n
    return fib(n-2) + fib(n-1)

