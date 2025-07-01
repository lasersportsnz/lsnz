import sqlalchemy as sa
import json
from flask import Response
from app import db
from app.api import bp
from app.models import Registration

@bp.route('/registrations', methods=['GET'])
def registrations():
    event_id = None
    from flask import request
    if 'event_id' in request.args:
        try:
            event_id = int(request.args['event_id'])
        except Exception:
            return Response(json.dumps({'error': 'Invalid event_id'}), status=400, mimetype='application/json')
    query = sa.select(Registration)
    if event_id is not None:
        query = query.where(Registration.event_id == event_id)
    regs = db.session.scalars(query).all()
    regs = [reg.to_dict() for reg in regs]
    return Response(json.dumps(regs), mimetype='application/json')