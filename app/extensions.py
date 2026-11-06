from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = "main.login"
login_manager.login_message = "Entre na sua conta para acessar esta página."
login_manager.login_message_category = "warning"
