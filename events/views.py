from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from sqlalchemy import asc

mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    exhibition = Event.query.filter(Event.category == 'Exhibition', Event.date >= date.today()).order_by(
        asc(Event.date)).limit(2)
    networking = Event.query.filter(Event.category == 'Networking', Event.date >= date.today()).order_by(
        asc(Event.date)).limit(2)
    recreation = Event.query.filter(Event.category == 'Recreation', Event.date >= date.today()).order_by(
        asc(Event.date)).limit(2)
    return render_template('index.html', exhibition=exhibition, networking=networking, recreation=recreation)

