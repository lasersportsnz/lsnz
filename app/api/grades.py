import json
from flask import Response
from app.models import Grade
from app.api import bp

@bp.route('/grades', methods=['GET'])
def get_grades():
    grades = Grade.query.order_by(Grade.points.desc()).all()
    return Response(json.dumps([grade.to_dict() for grade in grades]), mimetype='application/json')