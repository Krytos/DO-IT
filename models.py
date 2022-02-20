from app import app, db
from flask import session, url_for, redirect, flash
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.menu import MenuLink
from flask_mongoengine.wtf import model_form


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'  # Bootstrap design für das Admin interface


class MyModelView(ModelView):  # Decorator, welcher prüft ob ein admin eingeloggt ist
    def is_accessible(self):
        if "rights" in session:  # Schaut ob ein user mti rechten in session hinterlegt ist
            if session["rights"] == "admin":   # Prüft ob dieser nutzer admin rechte hat
                return True  # Sofern er admin rechte hat, wird True als is_accessible returned und Zugriff gewährt

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))  # Sofern es inaccassible ist, wird auf login redirected


class MyAdminIndexView(AdminIndexView):  # Filtert die Ansicht verschiedener nutzer, sofern man nicht-Admins zugriff
    def is_accessible(self):  # auf das Admin Interface gewähren möchte um z.B. den Fragebogen abzuändern
        if "rights" in session:
            if session["rights"] == "admin":
                return True  # Boolean of current_user to decide if logged in

    def inaccessible_callback(self, name, **kwargs):
        flash("No Admin rights!")
        return redirect(url_for("login"))


class LogoutMenuLink(MenuLink):  # Fügt einen Logout Button zum Admin Panel hinzu, wenn man in der session ist
    def is_accessible(self):
        if "user" in session:
            return True


class Users(db.Document):  # Erstellt die User Ansicht im Admin Panel und füllt sie mit Einträgen aus der Datenbank
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    pwhash = db.StringField(required=True, min_length=5)
    rights = db.StringField()


class Formular(db.Document):  # Erstellt die Formular Ansicht im Admin Panel und füllt sie
    question = db.StringField()  # mit Einträgen aus der Datenbank.
    answers = db.ListField(db.StringField())
    question_id = db.IntField()
    answer_id = db.ListField(db.StringField())
    form_type = db.StringField()
    alt = db.StringField()


class Contact(db.Document):  # Erstellt die Kunden Ansicht im Admin Panel und füllt Sie mit den Einträgen aus der
    datum = db.DateField()  # Datenbank
    vorname = db.StringField()
    nachname = db.StringField()
    email = db.EmailField()
    tel = db.StringField()
    add_info = db.StringField()


PostForm = model_form(Contact)  # Erstellt einträge in der Datenbank, mit der Contact class mit hilfe von mongoengine

admin = Admin(app, index_view=MyAdminIndexView(), name="Admin", template_mode='bootstrap3')
admin.add_view(MyModelView(Users, name="Users"))  # Erteils der class Users die ansicht Users
admin.add_view(MyModelView(Formular, name="Fragebogen"))  # ""
admin.add_view(MyModelView(Contact, name="Kunden"))  # ""
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))  # Fügt den Logout button hinzu