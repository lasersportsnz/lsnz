import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth
from app import db
from app.models import Player
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(email, password):
    player = db.session.scalar(sa.select(Player).where(Player.email == email))
    if player and player.check_password(password):
        return player

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)