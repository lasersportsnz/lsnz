import datetime
from flask import render_template, request
from flask_login import login_required, current_user
import sqlalchemy as sa
from sqlalchemy import func
from app import db
from app.models import Event, Site, Registration
from app.events import bp
from flask_wtf import FlaskForm
from wtforms import SubmitField

def event_slugify(name):
    return name.lower().replace(' ', '-')

@bp.route('/events')
def events():
    events = db.session.scalars(
        sa.select(Event).order_by(Event.date.desc()).limit(10)
    ).all()
    event_dicts = []
    for event in events:
        site = db.session.get(Site, event.site_id)
        event_dict = event.to_dict()
        event_dict['site_name'] = site.name if site else ''
        event_dicts.append(event_dict)
    return render_template('events/events.html', title='Events', events=event_dicts)

@bp.route('/events/<event_slug>')
def event_detail(event_slug):
    event = db.session.scalar(
        sa.select(Event)
        .where(func.lower(func.replace(Event.name, ' ', '-')) == event_slug.lower())
    )
    if not event:
        return render_template('text_page.html', title='Event Not Found', text_content='<p>Event not found.</p>'), 404
    site = db.session.get(Site, event.site_id)
    event_dict = event.to_dict()
    event_dict['site_name'] = site.name if site else ''
    is_future_event = False
    already_registered = False
    if event_dict.get('date'):
        try:
            event_date = datetime.date.fromisoformat(event_dict['date'])
            is_future_event = event_date > datetime.date.today()
        except Exception:
            pass
    # Check if user is logged in and already registered
    if current_user.is_authenticated:
        reg = db.session.scalar(
            sa.select(Registration).where(
                Registration.event_id == event.id,
                Registration.player_id == current_user.id
            )
        )
        already_registered = reg is not None
    registration_id = None
    if already_registered:
        reg = db.session.scalar(
            sa.select(Registration).where(
                Registration.event_id == event.id,
                Registration.player_id == current_user.id
            )
        )
        if reg:
            registration_id = reg.id
    return render_template('events/event.html', 
                           title=event.name, 
                           event=event_dict, 
                           is_future_event=is_future_event, 
                           already_registered=already_registered, 
                           registration_id=registration_id)

@bp.route('/events/<event_slug>/deregister', methods=['POST'])
@login_required
def event_deregister(event_slug):
    event = db.session.scalar(
        sa.select(Event)
        .where(func.lower(func.replace(Event.name, ' ', '-')) == event_slug.lower())
    )
    if not event:
        return render_template('text_page.html', title='Event Not Found', text_content='<p>Event not found.</p>'), 404
    reg = db.session.scalar(
        sa.select(Registration).where(
            Registration.event_id == event.id,
            Registration.player_id == current_user.id
        )
    )
    if reg:
        db.session.delete(reg)
        db.session.commit()
        return render_template('text_page.html', title='Deregistered', text_content=f'<p>You have been deregistered from {event.name}.')
    return render_template('text_page.html', title='Not Registered', text_content=f'<p>You are not registered for {event.name}.')

class EventRegisterForm(FlaskForm):
    submit = SubmitField('Register')

@bp.route('/events/<event_slug>/register', methods=['GET', 'POST'])
@login_required
def event_register(event_slug):
    event = db.session.scalar(
        sa.select(Event)
        .where(func.lower(func.replace(Event.name, ' ', '-')) == event_slug.lower())
    )
    if not event:
        return render_template('text_page.html', title='Event Not Found', text_content='<p>Event not found.</p>'), 404
    form = EventRegisterForm()
    if form.validate_on_submit():
        existing = db.session.scalar(
            sa.select(Registration).where(
                Registration.event_id == event.id,
                Registration.player_id == current_user.id
            )
        )
        if existing:
            return render_template('text_page.html', title='Already Registered', text_content=f'<p>You are already registered for {event.name}.')
        registration = Registration()
        registration.event_id = event.id
        registration.player_id = current_user.id
        registration.paid = False
        db.session.add(registration)
        db.session.commit()
        return render_template('text_page.html', title='Registered', text_content=f'<p>You are registered for {event.name}!')
    return render_template('events/register.html', title=f'Register for {event.name}', event=event, form=form)

# --- Sites list and detail routes ---
@bp.route('/sites')
def sites():
    sites = db.session.scalars(sa.select(Site).order_by(Site.name)).all()
    site_dicts = [site.to_dict() for site in sites]
    return render_template('events/sites.html', title='Sites', sites=site_dicts)

# Dynamic site detail page with human-readable slug
@bp.route('/sites/<site_slug>')
def site_detail(site_slug):
    site = db.session.scalar(
        sa.select(Site)
        .where(func.lower(func.replace(Site.name, ' ', '-')) == site_slug.lower())
    )
    if not site:
        return render_template('text_page.html', title='Site Not Found', text_content='<p>Site not found.</p>'), 404
    site_dict = site.to_dict()
    return render_template('events/site.html', title=site.name, site=site_dict)