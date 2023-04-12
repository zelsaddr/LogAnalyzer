from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class DomainForm(FlaskForm):
    domain = StringField('Domain', validators=[DataRequired()], render_kw={
        "placeholder": "example.com"})
    submit = SubmitField('Add Domain')


class LogFormUpload(FlaskForm):
    domain_id = HiddenField('Domain ID', validators=[DataRequired()])
    log = FileField('Upload New Log', validators=[DataRequired()])
    submit = SubmitField('Analyze Log')
