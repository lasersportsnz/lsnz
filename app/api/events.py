import sqlalchemy as sa
import json
from flask import Response
from app import db
from app.api import bp
from app.models import Event

@bp.route('/events', methods=['GET'])
def events():
    events = db.session.scalars(sa.select(Event)).all()
    events = [event.to_dict() for event in events]
    return Response(json.dumps(events), mimetype='application/json')
