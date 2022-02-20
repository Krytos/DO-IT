from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TelField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):  # Das Formular für das Login Fenster
    username = StringField('Username', validators=[DataRequired()])  # Validators um leeres Feld zu verhindern
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ContactForm(FlaskForm):  # Kontaktformular
    vorname = StringField("Vorname", validators=[DataRequired()])
    nachname = StringField("Nachname", validators=[DataRequired()])
    email = EmailField("E-Mail", validators=[DataRequired()])
    tel = TelField("Tel.:")
    add_info = TextAreaField("Weitere Infos:")
    file = FileField()
    submit = SubmitField('Abschicken')