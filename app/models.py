from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Player(db.Model):
    __tablename__ = 'players'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    alias: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), nullable=True)
    grade: so.Mapped[Optional[str]] = so.mapped_column(sa.String(10), nullable=True)
    profile_picture: so.Mapped[Optional[str]] = so.mapped_column(sa.String(200), nullable=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    
    def to_dict(self):
        """Return object data in easily serialisable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'alias': self.alias,
            'grade': self.grade
        }

    def __repr__(self):
        return f'<Player {self.name}>'
    
class Site(db.Model):
    __tablename__ = 'sites'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    country: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    address: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=False)
    system: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)

    def __repr__(self):
        return f'<Site {self.name} in {self.country}>'

class Event(db.Model):
    __tablename__ = 'events'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    site_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('sites.id'), nullable=False, index=True)
    date: so.Mapped[Optional[sa.Date]] = so.mapped_column(sa.Date, nullable=True)
    points_cap: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    format: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)

    def __repr__(self):
        return f'<Event {self.name} at {self.site_id}>'

class Registration(db.Model):
    __tablename__ = 'registrations'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('events.id'), nullable=False, index=True)
    player_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('players.id'), nullable=False, index=True)
    team_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('teams.id'), nullable=True, index=True)
    paid: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Registration for Event {self.event_id} by Player {self.player_id}>'
    
class Team(db.Model):
    __tablename__ = 'teams'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('events.id'), nullable=False, index=True)

    def __repr__(self):
        return f'<Team {self.name} for Event {self.event_id}>'
    
class Post(db.Model):
    __tablename__ = 'posts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('players.id'), nullable=False, index=True)

    def __repr__(self):
        return f'<Post {self.title} by {self.author_id}>'
    