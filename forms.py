from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo
from flask_wtf.file import FileRequired, FileAllowed, FileField

class RegistrationForm(FlaskForm):
    username = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Enter a Username"})
    password1 = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Enter a password"})
    password2 = PasswordField(
        validators=[InputRequired(), EqualTo("password1")],
        render_kw={"placeholder": "Confirm password:"})
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Username"})
    password = PasswordField(
        validators=[InputRequired()], 
        render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    image = FileField('file', 
        validators=[InputRequired(), FileAllowed(['jpg', 'png'], 'images only!')],)
    caption = StringField(
        render_kw={"placeholder":"Enter a caption"})
    submit = SubmitField("Post")

class SearchForm(FlaskForm):
    username = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Enter a username"})
    submit = SubmitField("Search")