from flask import Blueprint, render_template, request, redirect, url_for
from .models import Order
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bp.route('/')
@login_required
def show():
    orders = Order.query.filter_by(user_id=current_user.id)
    return render_template('history.html', orders=orders)