import os
from flask import render_template, request, jsonify, Response
import sqlalchemy as sa
from app import db
from app.models import Player
from app.main import bp

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'content')

def load_content(filename):
    with open(os.path.join(CONTENT_DIR, filename), encoding='utf-8') as f:
        return f.read()

@bp.route('/')
def serve_page(): 
    return render_template('base.html', title='Home', request=request)

@bp.route('/play')
def play():
    play_text = load_content('play.html')
    return render_template('text_page.html', title='Play', text_content=play_text)

@bp.route('/play/events')
def events():
    events = [
        {
            'site': {'country': 'Australia'},
            'body': 'Oceanic Champs 2025'
        },
        {
            'site': {'country': 'New Zealand'},
            'body': 'ZLTAC 2026'
        }
    ]
    return render_template('events.html', title='Events', events=events)

@bp.route('/play/leagues')
def leagues():
    leagues_text = load_content('leagues.html')
    return render_template('text_page.html', title='Leagues', text_content=leagues_text)

@bp.route('/play/formats')
def formats():
    results_text = ""
    return render_template('text_page.html', title='Game Formats', text_content=results_text)

@bp.route('/play/guides')
def guides():
    guides_text = ""
    return render_template('text_page.html', title='Guides to Improving', text_content=guides_text)

@bp.route('/results')
def results():
    results_text = ""
    return render_template('text_page.html', title='Results', text_content=results_text)
    
@bp.route('/results/invitationals')
def invitationals():
    results_text = ""
    return render_template('text_page.html', title='Invitationals', text_content=results_text)
    
@bp.route('/results/zltac')
def zltac():
    results_text = ""
    return render_template('text_page.html', title='ZLTAC', text_content=results_text)

@bp.route('/results/worlds')
def worlds():
    results_text = ""
    return render_template('text_page.html', title='Worlds', text_content=results_text)
    
@bp.route('/gallery')
def gallery():
    results_text = ""
    return render_template('text_page.html', title='Gallery', text_content=results_text)
    
@bp.route('/resources')
def resources():
    results_text = ""
    return render_template('text_page.html', title='Resources', text_content=results_text)

@bp.route('/blog')
def blog():
    posts = [
        {
            'author': {'username': 'Louis'},
            'body': 'Laser tag is fun!'
        },
        {
            'author': {'username': 'Rachel'},
            'body': 'Here\'s why you should play laser tag: it\'s a great way to exercise and have fun!'
        }
    ]
    return render_template('blog.html', title='Blog', user=user, posts=posts)


@bp.route('/about')
def about():
    about_text = load_content('about.html')
    return render_template('text_page.html', title='About Us', text_content=about_text)

@bp.route('/terms')
def terms():
    terms_text = load_content('terms.html')
    return render_template('text_page.html', title='Terms of Service', text_content=terms_text)

@bp.route('/privacy')
def privacy():
    privacy_text = load_content('privacy.html')
    return render_template('text_page.html', title='Privacy Policy', text_content=privacy_text)


