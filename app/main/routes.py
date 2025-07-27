import os
import datetime
import markdown
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from app.auth.identity import admin_permission
import sqlalchemy as sa
from sqlalchemy import func
from app import db
from app.models import Player, Grade, Event, Site, Post
from app.main import bp
from app.main.forms import EditProfileForm, PostForm

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'content')

def load_content(filename) -> str:
    with open(os.path.join(CONTENT_DIR, filename), encoding='utf-8') as f:
        return markdown.markdown(f.read())

@bp.route('/')
def home(): 
    return render_template('base.html', title='Home', request=request)

@bp.route('/play')
def play():
    play_text = load_content('play.md')
    return render_template('text_page.html', title='Play', text_content=play_text)

@bp.route('/play/leagues')
def leagues():
    leagues_text = load_content('leagues.md')
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
    query = sa.select(Post).order_by(Post.timestamp.desc())
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False)
    next_url = url_for('main.blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.blog', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('blog.html', title='Blog', posts=posts.items,
                        next_url=next_url, prev_url=prev_url)

@bp.route('/blog/<post_slug>')
def blog_post(post_slug):
    post = db.first_or_404(
        sa.select(Post)
        .where(func.lower(func.replace(Post.title, ' ', '-')) == post_slug.lower())
    )
    markdown_content = markdown.markdown(post.body)

    return render_template('post.html', title=post.title, post=post, content=markdown_content)

@bp.route('/blog/<post_slug>/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def edit_blog_post(post_slug):
    post = db.first_or_404(
        sa.select(Post)
        .where(func.lower(func.replace(Post.title, ' ', '-')) == post_slug.lower())
    )
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Your post has been updated.')
        return redirect(url_for('main.blog_post', post_slug=post_slug))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('post_editor.html', title=post.title, form=form)

@bp.route('/blog/post', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def write_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.write_post'))
    return render_template('post_editor.html', title='Editor', form=form)

@bp.route('/about')
def about():
    about_text = load_content('about.md')
    return render_template('text_page.html', title='About Us', text_content=about_text)

@bp.route('/terms')
def terms():
    terms_text = load_content('terms.md')
    return render_template('text_page.html', title='Terms of Service', text_content=terms_text)

@bp.route('/privacy')
def privacy():
    privacy_text = load_content('privacy.md')
    return render_template('text_page.html', title='Privacy Policy', text_content=privacy_text)

@bp.route('/players')
def players():
    grades = db.session.scalars(sa.select(Grade).order_by(Grade.points.desc())).all()
    players = db.session.scalars(
        sa.select(Player)
        .join(Grade, Player.grade_id == Grade.id)
        .order_by(Grade.points.desc())
    ).all()
    return render_template('players.html', title='Player List', 
                           players=players,
                           grades=grades)

@bp.route('/players/<alias>')
def player(alias):
    player = db.first_or_404(sa.select(Player).where(func.lower(Player.alias) == alias.lower()))
    posts = db.session.scalars(player.posts.select()).all()
    return render_template('player.html', player=player, posts=posts)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.alias)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.alias = form.alias.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.alias.data = current_user.alias
        form.bio.data = current_user.bio
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)