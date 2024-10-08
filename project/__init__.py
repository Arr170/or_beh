from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import logging

from werkzeug.security import generate_password_hash
import os



if(os.environ['IS_PROD']=='1'):
    COMP_PATH = '/project/data'#upravit podle umisteni na servru
else:
    COMP_PATH = './project/data'

db = SQLAlchemy()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s : %(message)s',
)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s'))
logging.getLogger().addHandler(file_handler)

logger = logging.getLogger(__name__)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(file_handler)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jsemlinygenerovat'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(),COMP_PATH, 'users.db')


    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

    from .models import User, Result, Track, Point, Event

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # stranka nebude mit funkcionalitu vytvorit novy uzivatelsky profil, proto jediny profil bude vytvoreny pri inicializaci
    # mail i heslo budou ulozeny v env souboru, pripadne hosting casto nabizi vytvoreni secret env
    with app.app_context():
        user = User.query.filter_by(email = os.environ["ADMIN_MAIL"]).first() # aby nevznikala chyba pri opakovanem zpusteni stranky bez mazani db

        if not user: 
            
            init_admin = User(email = os.environ["ADMIN_MAIL"], name = "Admin",password=generate_password_hash(os.environ["ADMIN_PASS"], method='pbkdf2:sha1') )
            db.session.add(init_admin)
            db.session.commit()  

        ev = Event.query.get(1)
        if not ev:
            init_ev = Event(name = "Název eventu")
            db.session.add(init_ev)
            db.session.commit()

        # #Create a new track
        # new_track = Track(name='Track1')
        # db.session.add(new_track)
        # db.session.commit()

        # # Create points associated with the track
        # point1 = Point(number=1, track_id=new_track.id)
        # point2 = Point(number=2, track_id=new_track.id)
        # db.session.add(point1)
        # db.session.add(point2)
        # db.session.commit()

    @app.before_request
    def log_request_info():
        logger.info('Request: %s %s', request.method, request.url)

      # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)    

    return app


