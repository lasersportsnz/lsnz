import sqlalchemy as sa
import json
from flask import request, Response
from app import db
from app.api import bp
from app.models import Site

@bp.route('/sites/<int:id>', methods=['GET'])
def get_site(id):
    return db.get_or_404(Site, id).to_dict()

@bp.route('/sites', methods=['GET'])
def get_sites():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Site.to_collection_dict(sa.select(Site), page, per_page,
                                    'api.get_sites')

