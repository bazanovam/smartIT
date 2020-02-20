from flask import render_template
from ..models import Request
from . import main


@main.route('/')
def index():
    requests = Request.query.count()
    return render_template('index.html', requests=requests)
