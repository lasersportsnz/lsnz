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
    # Prepopulate grades
    grade_data = [
        dict(letter='A', points=7, description='Players at the highest level in NZ.'),
        dict(letter='BB', points=6, description='Experienced players approaching the top level in NZ.​'),
        dict(letter='B', points=5, description='Experienced players with well rounded skills.​'),
        dict(letter='C', points=4, description='Players with pack skills and basic tactics.​'),
        dict(letter='D', points=3, description='Players with some basic pack skills.​'),
        dict(letter='E+', points=1, description='Players developing pack skills'),
        dict(letter='E', points=0, description='New players'),
    ]
    for g in grade_data:
        grade = Grade.query.filter_by(letter=g['letter']).first()
        if not grade:
            grade = Grade()
            grade.letter = g['letter']
            grade.points = g['points']
            grade.description = g['description']
            db.session.add(grade)
    db.session.commit()

    # Prepopulate sites from JSON
    sites_path = os.path.join(os.path.dirname(__file__), 'sites.json')
    with open(sites_path, encoding='utf-8') as f:
        sites_data = json.load(f)
    for s in sites_data:
        site = Site.query.filter_by(name=s['name']).first()
        if not site:
            site = Site(
                name=s['name'],
                country=s['country'],
                address=s['address'],
                system=s['system']
            )
            db.session.add(site)
    db.session.commit()

    # Prepopulate events from JSON
    events_path = os.path.join(os.path.dirname(__file__), 'events.json')
    with open(events_path, encoding='utf-8') as f:
        events_data = json.load(f)
    for e in events_data:
        site = Site.query.filter_by(name=e['site_name']).first()
        event = Event.query.filter_by(name=e['name']).first()
        if not event and site:
            event = Event(
                name=e['name'],
                site_id=site.id,
                date=datetime.strptime(e['date'], '%Y-%m-%d').date(),
                points_cap=e['points_cap'],
                format=e['format']
            )
            db.session.add(event)
    db.session.commit()

    # Prepopulate users
    users = [
        dict(first_name='Louis', last_name='Habberfield-Short', email='admin@example.com', alias='Tradey', grade='B', password='adminpass', is_admin=True,
             bio='Great at getting denied.',
             profile_picture='https://randomuser.me/api/portraits/men/1.jpg',
             playing_since=date(2015, 1, 1)),
        dict(first_name='Jono', last_name='Scott', email='louis@example.com', alias='Mouldy', grade='A', password='testpass', is_admin=False,
             bio='Dislikes people throwing games.',
             profile_picture='https://randomuser.me/api/portraits/men/2.jpg',
             playing_since=date(2018, 6, 15)),
        dict(first_name='Rachel', last_name='Scott', email='rachel@example.com', alias='Cheru', grade='B', password='testpass', is_admin=False,
             bio='Great at teaching new players.',
             profile_picture='https://randomuser.me/api/portraits/women/3.jpg',
             playing_since=date(2022, 3, 10)),
    ]
    for u in users:
        player = Player.query.filter_by(email=u['email']).first()
        if not player:
            player = Player()
            player.first_name = str(u['first_name'])
            player.last_name = str(u['last_name'])
            player.email = str(u['email'])
            player.alias = str(u['alias'])
            grade_obj = Grade.query.filter_by(letter=u['grade']).first()
            player.grade = grade_obj
            player.roles = 'admin' if u.get('is_admin') else ''
            player.bio = str(u['bio'])
            player.profile_picture = str(u['profile_picture'])
            player.playing_since = u['playing_since']
            player.set_password(u['password'])
            db.session.add(player)
    db.session.commit()
    click.echo('Prepopulated users, grades, sites, and events added.')
