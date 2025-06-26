from flask import Blueprint

bp = Blueprint('events', __name__, url_prefix='/play')

from app.events import routes
