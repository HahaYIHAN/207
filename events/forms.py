from flask_wtf import FlaskForm
from wtforms.fields import DateTimeField, TextAreaField, SubmitField, SelectField, StringField, PasswordField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed
from datetime import datetime
from wtforms.widgets import TextArea

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}


class EventForm(FlaskForm):
    name = StringField('Country', validators=[InputRequired()])
    description = TextAreaField('Description', widget=TextArea(),
                                validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    price = StringField('Price', validators=[InputRequired()])
    tickets = IntegerField('Tickets', validators=[InputRequired()])
    category = SelectField('Category', validators=[InputRequired()], choices=[
                           ('Exhibition', 'Exhibition'), ('Recreation', 'Recreation'), ('Networking', 'Networking')])
    status = SelectField('Status', validators=[InputRequired()], choices=[
        ('Open', 'Open'), ('Unpublished', 'Unpublished'), ('Sold-out', 'Sold-out'), ('Cancelled', 'Cancelled')])
    email = StringField('email', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    website = StringField('website', validators=[InputRequired()])
    address = StringField('address', validators=[InputRequired()])
    date = DateTimeField(
        "Date", format="%Y-%m-%dT%H:%M",
        default=datetime.today,
        validators=[DataRequired()]
    )
    submit = SubmitField("Create")


class UpdateForm(FlaskForm):
    name = StringField('Country', validators=[InputRequired()])
    description = TextAreaField('Description', widget=TextArea(),
                                validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
    price = StringField('Price', validators=[InputRequired()])
    tickets = IntegerField('Tickets', validators=[InputRequired()])
    category = SelectField('Category', validators=[InputRequired()], choices=[
                           ('Exhibition', 'Exhibition'), ('Recreation', 'Recreation'), ('Networking', 'Networking')])
    status = SelectField('Status', validators=[InputRequired()], choices=[
        ('Open', 'Open'), ('Unpublished', 'Unpublished'), ('Inactive', 'Inactive'), ('Cancelled', 'Cancelled')])
    email = StringField('email', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    website = StringField('website', validators=[InputRequired()])
    address = StringField('address', validators=[InputRequired()])
    date = DateTimeField(
        "Date", format="%Y-%m-%dT%H:%M",
        default=datetime.today,
        validators=[DataRequired()]
    )
    submit = SubmitField("Update")
# User login


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

# User register


class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[
                        Email("Please enter a valid email")])
    number = IntegerField("Phone Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

# User comment


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')


class BookingForm(FlaskForm):
    count = IntegerField('Count', validators=[InputRequired()])
    submit = SubmitField('Make payment')
