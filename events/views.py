from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from sqlalchemy import asc

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    exhibition = Event.query.filter(Event.category == 'Exhibition').all()
    networking = Event.query.filter(Event.category == 'Networking').all()
    recreation = Event.query.filter(Event.category == 'Recreation').all()
    return render_template('index.html', exhibition=exhibition, networking=networking, recreation=recreation)

@mainbp.route('/search')
def search():
    if request.args['search']:
        e = "%" + request.args['search'] + '%'
        exhibition = Event.query.filter(Event.category == 'Exhibition', Event.description.like(e)).all()
        networking = Event.query.filter(Event.category == 'Networking', Event.description.like(e)).all()
        recreation = Event.query.filter(Event.category == 'Recreation', Event.description.like(e)).all()
        return render_template('index.html', exhibition=exhibition, networking=networking, recreation=recreation)
    else:
        return redirect(url_for('main.index'))