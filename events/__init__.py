from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
app=Flask(__name__)

def create_app():
    
    #we use this utility module to display forms quickly
    bootstrap = Bootstrap(app)

    #A secret key for the session object
    app.secret_key='somerandomvalue'

    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    #Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///events.sqlite'
    db.init_app(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.bp)
    from . import auth
    app.register_blueprint(auth.bp)
    from .import bookings
    app.register_blueprint(bookings.bp)
    return app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_errors(e):
    return render_template('500.html'), 500