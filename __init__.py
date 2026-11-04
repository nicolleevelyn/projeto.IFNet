from pathlib import Path
from flask import Flask
from config import Config
from app.extensions import db, login_manager, csrf
from sqlalchemy import inspect, text


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import models
    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        columns = {
            column["name"]
            for column in inspect(db.engine).get_columns("material")
        }

        if "order_index" not in columns:
            with db.engine.begin() as connection:
                connection.execute(
                    text(
                        "ALTER TABLE material "
                        "ADD COLUMN order_index INTEGER NOT NULL DEFAULT 1"
                    )
                )

    return app
