import sqlalchemy as sa
import json
from flask import request
from app import db
from app.api import bp
from app.models import Event

@bp.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    return db.get_or_404(Event, id).to_dict()

@bp.route('/events', methods=['GET'])
def get_events():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Event.to_collection_dict(sa.select(Event), page, per_page,
                                  endpoint='api.get_events')
