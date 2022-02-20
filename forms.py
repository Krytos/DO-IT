from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TelField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ContactForm(FlaskForm):
    vorname = StringField("Vorname", validators=[DataRequired()])
    nachname = StringField("Nachname", validators=[DataRequired()])
    email = EmailField("E-Mail", validators=[DataRequired()])
    tel = TelField("Tel.:")
    add_info = TextAreaField("Weitere Infos:")
    file = FileField()
    submit = SubmitField('Abschicken')