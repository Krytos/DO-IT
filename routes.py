from flask import render_template, redirect, url_for, flash, session, request
from app import app, question_answer, current_page
from forms import LoginForm, ContactForm
from models import Formular, Contact, PostForm
from datetime import datetime, date, timedelta
from werkzeug.security import check_password_hash

today = date.today()
now = datetime.now()
db = app.db
users = app.db.users
app.permanent_session_lifetime = timedelta(days=30)

print(today)
def beratung(self, text):
    post_form = PostForm(request.form)
    get_form = ContactForm()
    if request.method == "POST" and post_form.validate():
        question_answer["Name"] = str(get_form.vorname.data), str(get_form.nachname.data)
        file = open(f"{question_answer['Name'][1]}_{question_answer['Name'][0]}_{today}.txt", "w+")
        for key, value in question_answer.items():
            file.write(f"Frage: {key}\nAntwort: {value}\n\n")
        file.close()
        # db.antworten.insert(question_answer)
        contactdata = Contact(
            datum = today.isoformat(),
            vorname = get_form.vorname.data,
            nachname = get_form.nachname.data,
            email = get_form.email.data,
            tel = get_form.tel.data,
            add_info = get_form.add_info.data,
        )
        contactdata.save()

        return redirect(url_for("index"))

    if self is None:
        self = 0  # 12121211
    if text is None:
        text = 0
    if self == 11211 and text > 2:
        next_question = int(str(self) + str(2))
    else:
        next_question = self
    back = current_page()
    question = Formular.objects.get(question_id=next_question).question
    form_type = Formular.objects.get(question_id=next_question).form_type
    if form_type != "contact":
        answers = Formular.objects.get(question_id=next_question).answers
        answer_id = Formular.objects.get(question_id=next_question).answer_id
        alt = Formular.objects.get(question_id=next_question).alt
        answer = zip(answers, answer_id)
        return render_template("beratung.html", answer=answer, question=question, q_id=self,
                               form_type=form_type, back=back, alt=alt)
    else:
        return render_template("beratung.html", question=question, q_id=self,
                               form_type=form_type, form=get_form)  # TODO: FIx CSS for contact form


# TODO: Redirect /admin to login, if user is not logged in.

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect("/admin/")
    form = LoginForm()
    if form.validate_on_submit():
        user = users.find_one({"username": form.username.data})
        if user:
            if check_password_hash(user["pwhash"], form.password.data):
                if form.remember_me:
                    session.permanent = True
                session["user"] = form.username.data
                session["rights"] = user["rights"]
                return redirect("/admin/")
        else:
            flash("Wrong Username / Password.")
            return render_template('login.html', title='Sign In', form=form)
        # return render_template('login.html', title='Sign In', form=form)
    else:
        return render_template('login.html', title='Sign In', form=form)

@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))