import sqlalchemy as sa
import json
from flask import request, Response
from app import db
from app.api import bp
from app.models import Player

@bp.route('/players', methods=['GET'])
def players():
    players = db.session.scalars(sa.select(Player)).all()
    players = [player.to_dict() for player in players]
    return Response(json.dumps(players), mimetype='application/json')