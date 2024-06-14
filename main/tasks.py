from operator import itemgetter
import requests
from tg_interface.celery import app
import shutil



@app.task()
def get_updates():
    pass
