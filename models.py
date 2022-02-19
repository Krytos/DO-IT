from app import app, db
from flask import session, url_for, redirect, flash
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.menu import MenuLink
from flask_mongoengine.wtf import model_form


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


class MyModelView(ModelView):
    def is_accessible(self):
        if "rights" in session:
            if session["rights"] == "admin":
                return True  # Boolean of current_user to decide if logged in

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if "rights" in session:
            if session["rights"] == "admin":
                return True  # Boolean of current_user to decide if logged in

    def inaccessible_callback(self, name, **kwargs):
        flash("No Admin rights!")
        return redirect(url_for("login"))


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        if "user" in session:
            return True


class Users(db.Document):
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    pwhash = db.StringField(required=True, min_length=5)
    rights = db.StringField()


class Formular(db.Document):
    question = db.StringField()
    answers = db.ListField(db.StringField())
    question_id = db.IntField()
    answer_id = db.ListField(db.StringField())
    form_type = db.StringField()
    alt = db.StringField()


class Contact(db.Document):
    datum = db.DateField()
    vorname = db.StringField()
    nachname = db.StringField()
    email = db.EmailField()
    tel = db.StringField()
    add_info = db.StringField()


PostForm = model_form(Contact)

admin = Admin(app, index_view=MyAdminIndexView(), name="Admin", template_mode='bootstrap3')
admin.add_view(MyModelView(Users, name="Users"))
admin.add_view(MyModelView(Formular, name="Fragebogen"))
admin.add_view(MyModelView(Contact, name="Kunden"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))