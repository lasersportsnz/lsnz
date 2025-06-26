import sqlalchemy as sa
import json
from flask import Response
from app import db
from app.api import bp
from app.models import Registration

@bp.route('/registrations', methods=['GET'])
def registrations():
    regs = db.session.scalars(sa.select(Registration)).all()
    regs = [reg.to_dict() for reg in regs]
    return Response(json.dumps(regs), mimetype='application/json')
