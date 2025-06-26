import sqlalchemy as sa
import json
from flask import request, Response
from app import db
from app.api import bp
from app.models import Site

@bp.route('/sites', methods=['GET'])
def sites():
    sites = db.session.scalars(sa.select(Site)).all()
    sites = [site.to_dict() for site in sites]
    return Response(json.dumps(sites), mimetype='application/json')

@bp.route('/sites/<int:id>', methods=['GET'])
def get_site(id):
    site = db.session.get(Site, id)
    if site is None:
        return Response(json.dumps({'error': 'Site not found'}), status=404, mimetype='application/json')
    return Response(json.dumps(site.to_dict()), mimetype='application/json')
