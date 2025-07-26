import sqlalchemy as sa
import json
from flask import request, url_for
from app import db
from app.api import bp
from app.models import Player
from app.api.errors import bad_request

@bp.route('/players/<int:id>', methods=['GET'])
def get_player(id):
     return db.get_or_404(Player, id).to_dict()

@bp.route('/players', methods=['GET'])
def get_players():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Player.to_collection_dict(sa.select(Player), page, per_page,
                                      'api.get_players')

@bp.route('/players', methods=['POST'])
def create_player():
    data = request.get_json()
    if 'first_name' not in data or 'last_name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include first name, last name, email and password fields')
    if db.session.scalar(sa.select(Player).where(
            Player.alias == data['alias'])):
        return bad_request('please use a different alias')
    if db.session.scalar(sa.select(Player).where(
            Player.email == data['email'])):
        return bad_request('please use a different email address')
    player = Player()
    player.from_dict(data, new_user=True)
    db.session.add(player)
    db.session.commit()
    return player.to_dict(), 201, {'Location': url_for('api.get_player',
                                                     id=player.id)}

@bp.route('/players/<int:id>', methods=['PUT'])
def update_player(id):
    player = db.get_or_404(Player, id)
    data = request.get_json()
    if 'alias' in data and data['alias'] != player.alias and \
        db.session.scalar(sa.select(Player).where(
            Player.alias == data['alias'])):
        return bad_request('please use a different alias')
    if 'email' in data and data['email'] != player.email and \
        db.session.scalar(sa.select(Player).where(
            Player.email == data['email'])):
        return bad_request('please use a different email address')
    player.from_dict(data, new_user=False)
    db.session.commit()
    return player.to_dict()
