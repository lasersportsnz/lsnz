from typing import Optional
from datetime import date
from collections import namedtuple
from functools import partial
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class Player(UserMixin, db.Model):
    __tablename__ = 'players'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True, index=True)
    alias: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20))
    grade_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('grades.id'), index=True, nullable=False)
    grade: so.Mapped[Optional['Grade']] = so.relationship('Grade', back_populates='players')
    profile_picture: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))
    playing_since: so.Mapped[Optional[sa.Date]] = so.mapped_column(sa.Date)
    bio: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    roles: so.Mapped[str] = so.mapped_column(sa.String(128))  # Comma-separated roles
    posts = so.relationship('Post', back_populates='author')
    registrations = so.relationship('Registration', back_populates='player')

    def __init__(self, *args, grade=None, playing_since=None, **kwargs):
        super().__init__(*args, **kwargs)
        if grade is None:
            self.set_starting_grade()
        else:
            self.grade = grade
        if playing_since is None:
            self.playing_since = date.today()
        else:
            self.playing_since = playing_since

    def set_starting_grade(self):
        # Start at grade with the lowest points
        lowest_grade = db.session.query(Grade).order_by(Grade.points.asc()).first()
        self.grade = lowest_grade if lowest_grade else None
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def from_dict(self, data, new_user=False):
        for field in ['first_name', 
                      'last_name', 
                      'email', 
                      'alias', 
                      'profile_picture', 
                      'bio', 
                      'roles']:
            if field in data:
                setattr(self, field, data[field])
        if new_user:
            if 'password' in data:
                self.set_password(data['password'])
            if 'grade_id' in data:
                self.grade = db.session.get(Grade, data['grade_id'])
            elif 'grade' in data:
                self.grade = db.session.query(Grade).filter_by(letter=data['grade']).first()
            else:
                self.set_starting_grade()

    def to_dict(self):
        """Return object data in easily serialisable format"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'alias': self.alias,
            'grade': self.grade.letter if self.grade else None,
            'profile_picture': self.profile_picture,
            'playing_since': self.playing_since.isoformat() if self.playing_since else None,
            'bio': self.bio,
            'roles': self.roles
        }

    def __repr__(self):
        return f'<Player {self.first_name} {self.last_name}>'

    @login.user_loader
    def load_user(id):
        return db.session.get(Player, int(id))
    
class Grade(db.Model):
    __tablename__ = 'grades'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    letter: so.Mapped[str] = so.mapped_column(sa.String(10), unique=True, index=True)
    points: so.Mapped[int] = so.mapped_column(sa.Integer, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200))
    players = so.relationship('Player', back_populates='grade')

    def from_dict(self, data):
        for field in ['letter', 'points', 'description']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        """Return object data in easily serialisable format"""
        return {
            'id': self.id,
            'letter': self.letter,
            'points': self.points,
            'description': self.description
        }
    
    def __repr__(self):
        return f'<Grade {self.letter} worth {self.points} points>'
    
class Site(db.Model):
    __tablename__ = 'sites'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50))
    country: so.Mapped[str] = so.mapped_column(sa.String(100))
    address: so.Mapped[str] = so.mapped_column(sa.String(200))
    system: so.Mapped[str] = so.mapped_column(sa.String(50))

    def from_dict(self, data):
        for field in ['name', 'country', 'address', 'system']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'address': self.address,
            'system': self.system
        }

    def __repr__(self):
        return f'<Site {self.name} in {self.country}>'

class Event(db.Model):
    __tablename__ = 'events'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50))
    site_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('sites.id'), index=True)
    date: so.Mapped[Optional[sa.Date]] = so.mapped_column(sa.Date)
    points_cap: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    format: so.Mapped[str] = so.mapped_column(sa.String(50))
    registrations = so.relationship('Registration', backref='event', cascade='all, delete-orphan')

    def from_dict(self, data):
        for field in ['name', 'site_id', 'date', 'points_cap', 'format']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'site_id': self.site_id,
            'date': self.date.isoformat() if self.date else None,
            'points_cap': self.points_cap,
            'format': self.format
        }

    def __repr__(self):
        return f'<Event {self.name} at {self.site_id}>'

class Registration(db.Model):
    __tablename__ = 'registrations'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('events.id'), index=True)
    player_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('players.id'), index=True)
    player: so.Mapped['Player'] = so.relationship('Player', back_populates='registrations')
    team_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('teams.id'), index=True)
    paid: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)

    def from_dict(self, data):
        for field in ['event_id', 'player_id', 'team_id', 'paid']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'player_id': self.player_id,
            'team_id': self.team_id,
            'paid': self.paid
        }

    def __repr__(self):
        return f'<Registration for Event {self.event_id} by Player {self.player_id}>'
    
class Team(db.Model):
    __tablename__ = 'teams'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50))
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('events.id'), index=True)

    def from_dict(self, data):
        for field in ['name', 'event_id']:
            if field in data:
                setattr(self, field, data[field])
                
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'event_id': self.event_id
        }

    def __repr__(self):
        return f'<Team {self.name} for Event {self.event_id}>'
    
class Post(db.Model):
    __tablename__ = 'posts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(50))
    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('players.id'), nullable=False)
    author: so.Mapped['Player'] = so.relationship('Player', back_populates='posts')

    def from_dict(self, data):
        for field in ['title', 'author_id']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'author': self.author.to_dict() if self.author else None
        }

    def __repr__(self):
        return f'<Post {self.title} by {self.author}>'
