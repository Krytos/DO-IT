from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from flask_mongoengine import MongoEngine


load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.db = Config.client.alex
db = MongoEngine(app)
question_answer = {"Name": "",}
back = []


def current_page():
    z = (request.form.get("input", type=int))
    if z is None:
        z = 0
    back.append(z)
    print(back)
    return back

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


from routes import beratung


@app.route('/beratung/', methods=["POST", "GET"])
def forms():
    f = request.form.getlist("input", type=int)
    text = request.form.get("text")
    if not f:
        f = [0]

    a_id = []
    for item in f:
        if item != 0:
            a = item % 10 -1
            a_id.append(a)
        else:
            pass
    if f != 0 and text is None:
        q_id = f[0] // 10
        id = app.db.formular.find_one({"question_id": q_id})
        q = id["question"]
        a = id["answers"]
        answers = []
        for x in a_id:
            answers.append(a[x])
            if len(a_id) == 1:
                str_answers = "".join(answers)
            else:
                str_answers = ", ".join(answers)
            question_answer[q] = str_answers
    else:
        q_id = f[0]
        id = app.db.formular.find_one({"question_id": q_id})
        q = id["question"]
        question_answer[q] = text


    question_id = request.form.get("input", type=int)
    if question_id is None:
        question_id = 0
    print(question_id, question_answer)
    if 1121 < question_id < 1127:
        question_id = 1121
    if question_id == 21 and q in question_answer:
        question_id = 2111

    a = app.db.formular.find_one({"question_id":question_id})
    a_id = a["answer_id"][0]
    print(a_id)
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


# @app.route('/admin/', methods=["POST", "GET"])
# def admin():
#     return admin


if __name__ == '__main__':
    app.run()