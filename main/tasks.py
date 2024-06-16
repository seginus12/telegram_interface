from operator import itemgetter
import requests
from tg_interface.celery import app
import shutil




@app.task()
def check_updates():
    from .utils import get_updates
    get_updates()
