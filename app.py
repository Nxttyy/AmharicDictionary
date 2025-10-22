import sqlite3

from flask import Flask, render_template, request
from wtforms import Form, StringField, validators

from utils import parse_amharic_definitions, parse_dictionary_entry

app = Flask(__name__)


def getResult(word):
    conn = sqlite3.connect("ahun.sqlite")
    cursor = conn.cursor()

    word = (str(word),)
    cursor.execute("SELECT AMH, EN FROM dictionary WHERE _id=?", word)
    result = cursor.fetchall()

    return result


app = Flask(__name__)


class WordForm(Form):
    word = StringField("Word", validators=[validators.DataRequired()])


def case_correct_word(word):
    word = word.lower()
    return word[0].upper() + word[1:]


@app.route("/", methods=["GET", "POST"])
def home():
    form = WordForm(request.form)
    word = None

    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            word = case_correct_word(data.get("word", ""))
        elif form.validate():
            word = case_correct_word(form.word.data)

        if word:
            result = getResult(word)

            if result:
                result = result[0]
                amh, en = result
                amh = parse_amharic_definitions(amh)
                en = parse_dictionary_entry(en)

                return render_template(
                    "home.html",
                    form=form,
                    amh=amh,
                    en=en,
                    word=word,
                )
            else:
                return render_template(
                    "home.html",
                    form=form,
                    error=f"No Result for {word}, Check your spelling!",
                )
        else:
            return render_template(
                "home.html",
                form=form,
                error="Please enter a valid word!",
            )
    else:
        return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
