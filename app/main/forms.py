from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
import sqlalchemy as sa
from app import db
from app.models import Player

IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp')

class EditProfileForm(FlaskForm):
    first_name = StringField(('First Name'), validators=[DataRequired()])
    last_name = StringField(('Last Name'), validators=[DataRequired()])
    alias = StringField(('Alias'), validators=[DataRequired()])
    bio = TextAreaField(('Bio'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(('Submit'))

    def __init__(self, original_alias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_alias = original_alias

    def validate_alias(self, alias):
        if alias.data != self.original_alias:
            player = db.session.scalar(sa.select(Player).where(
                Player.alias == alias.data))
            if player is not None:
                raise ValidationError(('Please use a different alias.'))

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    image = FileField('Image', validators=[
        FileRequired('Please select an image.'),
        FileAllowed(IMAGE_EXTENSIONS, 'Images only!')
    ])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=1, max=200)])
    body = TextAreaField('Write your post using markdown format', validators=[
        DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField('Submit')