import sqlalchemy as sa
import json
from flask import request, Response
from app.api import bp
from app.models import Player

@bp.route('/players', methods=['GET'])
def players():
    players = [Player(name='Louis Habberfield-Short', alias='Tradey', grade='B'),
               Player(name='John Doe', alias='JD', grade='A')]
    players = [player.to_dict() for player in players]
    return Response(json.dumps(players), mimetype='application/json')