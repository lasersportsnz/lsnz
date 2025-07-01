import click
from flask import current_app
from flask.cli import with_appcontext
from app import db
from app.models import Player, Grade, Site, Event
from datetime import date, datetime
import os
import json

from app.cli import bp

@bp.cli.command('prepopulate')
@with_appcontext
def prepopulate():
    """Add initial users, grades, sites, and events to the database, including an admin."""
    # Drop and recreate all tables for a clean slate
    db.drop_all()
    db.create_all()

    # Prepopulate grades from JSON
    grades_path = os.path.join(os.path.dirname(__file__), 'grades.json')
    with open(grades_path, encoding='utf-8') as f:
        grade_data = json.load(f)
    for g in grade_data:
        grade = Grade()
        grade.from_dict(g)
        db.session.add(grade)
    db.session.commit()

    # Prepopulate sites from JSON
    sites_path = os.path.join(os.path.dirname(__file__), 'sites.json')
    with open(sites_path, encoding='utf-8') as f:
        sites_data = json.load(f)
    for s in sites_data:
        site = Site()
        site.from_dict(s)
        db.session.add(site)
    db.session.commit()

    # Prepopulate events from JSON
    events_path = os.path.join(os.path.dirname(__file__), 'events.json')
    with open(events_path, encoding='utf-8') as f:
        events_data = json.load(f)
    for e in events_data:
        # Attach site_id by looking up the site name
        site = Site.query.filter_by(name=e['site_name']).first()
        if site:
            event_dict = dict(e)
            event_dict['site_id'] = site.id
            event_dict.pop('site_name', None)
            # Convert date string to date object if needed
            if 'date' in event_dict and isinstance(event_dict['date'], str):
                event_dict['date'] = datetime.strptime(event_dict['date'], '%Y-%m-%d').date()
            event = Event()
            event.from_dict(event_dict)
            db.session.add(event)
    db.session.commit()

    # Prepopulate players from JSON
    players_path = os.path.join(os.path.dirname(__file__), 'players.json')
    with open(players_path, encoding='utf-8') as f:
        players = json.load(f)
    for p in players:
        user = Player()
        user.from_dict(p, new_user=True)
        db.session.add(user)
    db.session.commit()
    click.echo('Prepopulated players, grades, sites, and events added.')
