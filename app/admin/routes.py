from flask import render_template, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app.auth.identity import admin_permission
from app.models import Player, Grade
import sqlalchemy as sa
from app import db
from app.admin import bp

@bp.route('/')
@login_required
@admin_permission.require(http_exception=403)
def admin():
    return render_template('admin/admin.html', title='Admin Page')

@bp.route('/grades')
@login_required
@admin_permission.require(http_exception=403)
def grades():
    grades = db.session.scalars(sa.select(Grade).order_by(Grade.points.desc())).all()
    return render_template('admin/grades.html', title='Admin Grades', 
                           grades=grades)


# --- AJAX API for grade CRUD ---
@bp.route('/grades/create', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def create_grade():
    data = request.get_json()
    letter = data.get('letter', '').strip()
    points = data.get('points')
    description = data.get('description', '').strip()
    if not letter or points is None:
        return jsonify({'error': 'Letter and points are required'}), 400
    grade = Grade()
    grade.letter = letter
    grade.points = points
    grade.description = description
    db.session.add(grade)
    db.session.commit()
    return jsonify(grade.to_dict()), 201

@bp.route('/grades/update', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def update_grade():
    data = request.get_json()
    grade_id = data.get('id')
    grade = db.session.get(Grade, grade_id)
    if not grade:
        return jsonify({'error': 'Grade not found'}), 404
    grade.letter = data.get('letter', grade.letter)
    grade.points = data.get('points', grade.points)
    grade.description = data.get('description', grade.description)
    db.session.commit()
    return jsonify(grade.to_dict())

@bp.route('/grades/delete', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def delete_grade():
    data = request.get_json()
    grade_id = data.get('id')
    grade = db.session.get(Grade, grade_id)
    if not grade:
        return jsonify({'error': 'Grade not found'}), 404
    db.session.delete(grade)
    db.session.commit()
    return jsonify({'result': 'ok'})