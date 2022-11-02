from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, UpdateForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

bp = Blueprint('event', __name__, url_prefix='/events')


@bp.route('/<id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()
    booking = BookingForm()
    return render_template('events/show.html', event=event, booking=booking, form=cform)


# @bp.route('/search')
# def list():
#     if 'search' in request.args and request.args['search']:
#         key = "%" + request.args['search'] + '%'
#         events = Event.query.filter(
#             Event.description.like(key) | Event.name.like(key)).all()
#         return render_template('events/list.html', events=events, title=f"Search : {request.args['search']}")
#     if 'category' in request.args and request.args['category']:
#         events = Event.query.filter(
#             Event.category == request.args['category']).all()
#         return render_template('events/list.html', events=events, title=f"Category-{request.args['category']}")
#     else:
#         return redirect(url_for('main.index'))


@bp.route('booking/<id>',  methods=['POST'])
def booking(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    booking = BookingForm()
    if booking.validate_on_submit():
        count = booking.count.data
        if event.tickets < count:
            flash('Not enough tickets', 'danger')
            return redirect(url_for('event.show', id=event.id))
        else:
            event.tickets = event.tickets - count
            order = Order(
                user_id=current_user.id,
                event_id=event.id,
                count=count
            )
            db.session.add(order)
            db.session.add(event)
            # commit to the database
            db.session.commit()
            flash('Order has been made', 'success')
        return redirect(url_for('main.index'))
    return redirect(url_for('event.show', id=event.id))


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(name=form.name.data,
                      description=form.description.data,
                      image=db_file_path,
                      price=form.price.data,
                      email=form.email.data,
                      tickets=form.tickets.data,
                      category=form.category.data,
                      status=form.status.data,
                      phone=form.phone.data,
                      website=form.website.data,
                      address=form.address.data,
                      date=form.date.data,
                      user=current_user.id)
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        flash('Successfully created new travel event', 'success')
        # Always end with redirect when form is valid
        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    event = Event.query.filter_by(id=id).first()
    if event.user != current_user.id:
        flash('You are not allowed to edit this event', 'danger')
        return redirect(url_for('event.show', id=event.id))
    form = UpdateForm(obj=event)
    if form.validate_on_submit():

        file = check_upload_file(form)
        if file:
            event.image = file
        event.name = form.name.data
        event.description = form.description.data
        event.price = form.price.data
        event.email = form.email.data
        event.tickets = form.tickets.data
        event.category = form.category.data
        event.status = form.status.data
        event.phone = form.phone.data
        event.website = form.website.data
        event.address = form.address.data
        event.date = form.date.data
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event.show', id=event.id))

    return render_template('events/update.html', form=form, id=event.id)


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    if hasattr(fp, 'filename') == False:
        return None
    filename = fp.filename

    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/image', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


@bp.route('/<event>/comment', methods=['GET', 'POST'])
@login_required
def comment(event):
    form = CommentForm()
    # get the event object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data,
                          event=event_obj,
                          user=current_user)
        # here the back-referencing works - comment.event is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()

        # flashing a message which needs to be handled by the html
        #flash('Your comment has been added', 'success')
        print('Your comment has been added', 'success')
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=event))


@bp.route('/delete/<event_id>', methods=['GET'])
def delete(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event.user != current_user.id:
        flash('You are not allowed to delete this event', 'danger')
        return redirect(url_for('event.show', id=event.id))
    # remove all orders that related to the event
    Order.query.filter_by(event_id=event_id).delete()
    # remove all events that are related to the event
    Comment.query.filter_by(event_id=event_id).delete()
    # remove this event

    db.session.delete(event)
    db.session.commit()
    flash('Event has been removed successfully', 'success')
    return redirect(url_for('main.index'))
