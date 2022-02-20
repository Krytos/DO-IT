from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine

from config import Config

load_dotenv()

app = Flask(__name__)  # Weißt Flask der variable app zu
app.config.from_object(Config)  # Teilt Flask mit, dass die Config Optionen sich im Objekt Config.py befinden
app.db = Config.client.feller  # Weißt der Variable app.db die URI für die Datenbank zu
db = MongoEngine(app)  # Initiert Mongoengine
question_answer = {"Name": "",}  # Dictionary welches Frage + Antwort enthalten wird.
back = []  # Liste für die Back Taste


def current_page():  # Funktion für die Back taste
    z = (request.form.get("input", type=int))  # Ruft den Wert aus dem "input" Feld ab, bzw. die answer_id
    if z is None:  # Setzt auf null, falls None um einen type error zu umgehen
        z = 0
    back.append(z)  # Fügt die answer_id der Liste hinzu
    return back


@app.route('/', methods=["GET"])  # Flask decorator welcher für routes genutzt wird
def index():
    return render_template("index.html")  # Template render für index.html


from routes import beratung  # Wird erst hier importiert um einen circular import zu vermeiden


@app.route('/beratung/', methods=["POST", "GET"])
def forms():  # Funktion welche Antworten den Fragen zuordnet und diese dann in dem Dictionary abspeichert
    f = request.form.getlist("input", type=int)
    text = request.form.get("text")  # Nimmt wer aus Text Feldern. Diese haben keine antwort id
    if not f:
        f = [0]

    a_id = []  # Antwort ID liste
    for item in f:  # Da alle antworten in f hinterlegt sind, wird hier durch die liste nach IDs gesucht
        if item != 0:
            a = item % 10 -1 # Module 10 -1, da wird die antworten der zuvor Frage benötigen und der index bei 0 beginnt
            a_id.append(a)  # Antwort positionen im Datenbank Index werden in die Liste eingetragen
        else:
            pass
    if f != 0 and text is None:  # Sofern die Liste Antworten beinhaltet und es kein Text Feld gibt
        q_id = f[0] // 10  # Question ID durch division 10 von antwort_id mit rest 0 -> 12112 > 1211
        id = app.db.formular.find_one({"question_id": q_id})  # Datenbankeintrag der ID wird zugewiesen
        q = id["question"]  # Das question Field der Datenbank
        a = id["answers"]  # Das answers array der Datenbank
        answers = []  # List erstellt für answers array der Datenbank
        for x in a_id:  # Geht durch die werte in der a_id liste 0,1,2,3,etc und fügt den dazugehörigen Datenbankeintrag
            answers.append(a[x])  # der liste answers hinzu. Das erlaubt das hinzufügen von checkbox antworten
            if len(a_id) == 1:  # Konvertiert die Liste zu einem String
                str_answers = "".join(answers)
            else:  # Bei mehreren Antworten, wird ein Komma zwischen die Einträge in der Liste platziert
                str_answers = ", ".join(answers)
            question_answer[q] = str_answers   # Der Frage werden die richtigen antworten im Didctionary zugewiesen
    else:  # Falls die Antwort ein Textfeld ist, wird nicht der wert von "input" sondern von "text" genommen.
        q_id = f[0]
        id = app.db.formular.find_one({"question_id": q_id})
        q = id["question"]
        question_answer[q] = text

    # Hier gibt es ausnahmen für verschiedene Question IDs, welche zu einem anderem Zweig im baum springen.
    # Ich habe zwar mitlerweile eine bessere Lösung für das Problem gefunden, aber nicht die Zeit es einzubauen
    question_id = request.form.get("input", type=int)
    if question_id is None:
        question_id = 0
    if 1121 < question_id < 1127:
        question_id = 1121
    if question_id == 21 and q in question_answer:
        question_id = 2111
    # Hier wird entschieden welche Frage als nächstes dran kommt.
    a = app.db.formular.find_one({"question_id": question_id})
    a_id = a["answer_id"][0]
    text_input = request.form.get("text", type=int)
    datum = request.form.get("datum")  # TODO: Datum hinzufügen
    file = request.form.get("file")  # TODO: File upload ins formular einfügen
    if text_input is not None:
        if request.form.get("text", type=int) > 2 and question_id == 12121:
            return beratung(int(a_id), request.form.get("text", type=int))
        else:
            return beratung(int(a_id), request.form.get("text", type=int))
    elif request.form.get("text"):
        return beratung(int(a_id), request.form.get("text"))
    else:
        return beratung(question_id, request.form.get("text", type=int))

  # Initiert Flask

if __name__ == '__main__':
    def app_create():
        app.run()
