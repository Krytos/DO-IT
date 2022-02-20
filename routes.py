from flask import render_template, redirect, url_for, flash, session, request
from app import app, question_answer, current_page
from forms import LoginForm, ContactForm
from models import Formular, Contact, PostForm
from datetime import datetime, date, timedelta
from werkzeug.security import check_password_hash

today = date.today()  # speichert das heute datum ab
now = datetime.now()  # speichert die aktuelle Zeit ab
db = app.db
users = app.db.users  # macht es einfacher auf die collection "users" in der datenbank zuzugreifen
app.permanent_session_lifetime = timedelta(days=30)  # Setzt die session duration von "remember me" auf 30 Tage


def beratung(self, text):  # Funktion des Hauptformulars
    post_form = PostForm(request.form)
    get_form = ContactForm()  # Zuweisung von ContactForm() aus forms.py
    if request.method == "POST" and post_form.validate():  # Prüft ob POST request und um das Formular richtig
        # ausgefüllt ist. Dem Dictionary question_answers wird vor und nachname des nutzers hinzugefügt
        question_answer["Name"] = str(get_form.vorname.data), str(get_form.nachname.data)
        # Dictionary wird in einer Datei mit dem format nachname_vorname_datum abgespeichert
        file = open(f"{question_answer['Name'][1]}_{question_answer['Name'][0]}_{today}.txt", "w+")
        for key, value in question_answer.items():
            file.write(f"Frage: {key}\nAntwort: {value}\n\n")
        file.close()  # Schleife, die Frage und Antwort zusammen in jeweils eine Zeile steckt und abspeichert
        # Kontaktformular wird mit den Daten aus dem HTML Formular gefüllt.
        contactdata = Contact(
            datum = today.isoformat(),
            vorname = get_form.vorname.data,
            nachname = get_form.nachname.data,
            email = get_form.email.data,
            tel = get_form.tel.data,
            add_info = get_form.add_info.data,
        )
        contactdata.save()  # Es wird in der Datenbank abgespeichert.

        return redirect(url_for("index"))  # Redirect nach Index
    # Selbe Prüfung nach Fragen wie in app.py
    if self is None:
        self = 0  # 12121211
    if text is None:
        text = 0
    if self == 11211 and text > 2:
        next_question = int(str(self) + str(2))
    else:
        next_question = self
    back = current_page()  # Die Liste die in app.py generiert wird, wird hier back zugewiesen
    # Nutzt mongoengine um die Formulare für das HTML Template zu erstellen
    question = Formular.objects.get(question_id=next_question).question
    form_type = Formular.objects.get(question_id=next_question).form_type
    if form_type != "contact":  # Ignoriert die anderen Werte, falls es sich um ein Kontkatformular handelt
        answers = Formular.objects.get(question_id=next_question).answers
        answer_id = Formular.objects.get(question_id=next_question).answer_id
        alt = Formular.objects.get(question_id=next_question).alt
        answer = zip(answers, answer_id)
        # Erstellt ein render vom template beratung.html und füttert es mit den werten für die oben genannten varioablen
        return render_template("beratung.html", answer=answer, question=question, q_id=self,
                               form_type=form_type, back=back, alt=alt)
    else:
        return render_template("beratung.html", question=question, q_id=self,
                               form_type=form_type, form=get_form)  # TODO: FIx CSS for contact form


# TODO: Redirect /admin to login, if user is not logged in.

@app.route('/login/', methods=['GET', 'POST'])  # Routing für login
def login():  # login funktion
    if "user" in session:  # falls man bereits eingeloggt ist, redirect an admin
        return redirect("/admin/")
    form = LoginForm()  # zuweisung der loginform
    if form.validate_on_submit():
        user = users.find_one({"username": form.username.data})  # sucht nach dem eingetragenen nutzer in der DB
        if user:   # Falls vorhanden wird geprüft ob das passwort übereinstimmt
            if check_password_hash(user["pwhash"], form.password.data):  # hasht das passwort und vergleicht es
                if form.remember_me:  # Falls remember me angetickt ist, wird session auf permanent aka 30 tage gesetzt
                    session.permanent = True
                session["user"] = form.username.data  # Nutzer wird in der session hinterlegt
                session["rights"] = user["rights"]  # Nutzer Rechte werden in der session hinterlegt
                return redirect("/admin/")  # redirect zu admin
        else:
            flash("Wrong Username / Password.")  # Falls der Nutzer nicht gefunden wird: Fehlermeldung
            return render_template('login.html', title='Sign In', form=form)
    else:  # Falls Nutzer nicht in session, login template render
        return render_template('login.html', title='Sign In', form=form)

@app.route("/logout/")  # Funktion für logout. Löscht die session und leitet an login weiter.
def logout():
    session.clear()  # Löscht eventuell die session für alle Nutzer. Wird später geprüft.
    return redirect(url_for("login"))