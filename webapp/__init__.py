from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "commands.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = "Laureta24"  #Per a poder obrir la sessió
    #app.permanent_session_lifetime = timedelta(hours=5)  #Per si volem mantenir informació de la sessió
                                                          #més enllà del tancament del browser. Es fa creant
                                                          #sessions permanents.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix="/")
    

    from .models import Commands
    with app.app_context():
        create_database()

    return app

def create_database():
    if not path.exists("webapp/" + DB_NAME):
        db.create_all()