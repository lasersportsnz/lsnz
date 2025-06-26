import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, session
from urllib.parse import urlparse, urljoin
from flask_login import current_user, login_user, logout_user
from flask_principal import identity_changed, Identity, AnonymousIdentity
import sqlalchemy as sa
from app import db
from app.models import Player
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Player).where(Player.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(),
                                identity=Identity(user.id))
        next_page = request.args.get('next')
        if next_page and is_safe_url(next_page):
            return redirect(next_page)
        return redirect(url_for('main.home'))
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    
    next_page = request.args.get('next')
    if next_page and is_safe_url(next_page):
        return redirect(next_page)
    return redirect(url_for('main.home'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Player(first_name=form.first_name.data, 
                      last_name=form.last_name.data, 
                      alias=form.alias.data, 
                      email=form.email.data,
                      playing_since=datetime.date.today())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)