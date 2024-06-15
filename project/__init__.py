from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from werkzeug.security import generate_password_hash
import os



if(os.environ['IS_PROD']=='1'):
    COMP_PATH = '/project/data'#upravit podle umisteni na servru
else:
    COMP_PATH = './project/data'

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'jsemlinygenerovat'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(),COMP_PATH, 'users.db')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()

    from .models import User, Result

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

      # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)    

    return app