import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import Player, Grade, Site, Event, Team, Registration, Post

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 
            'Player': Player, 
            'Grade': Grade,
            'Site': Site,
            'Event': Event, 
            'Team': Team,
            'Registration': Registration, 
            'Post': Post}