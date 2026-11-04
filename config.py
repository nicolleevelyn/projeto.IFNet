import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-de-desenvolvimento-troque-antes-de-publicar")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'ifnet.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
