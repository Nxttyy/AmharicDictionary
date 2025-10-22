import sqlite3

from flask import Flask, render_template, request
from wtforms import Form, StringField, validators

# from .utils import format_result

app = Flask(__name__)


def getResult(word):
    conn = sqlite3.connect("ahun.sqlite")
    cursor = conn.cursor()

    word = (str(word),)
    cursor.execute("SELECT AMH, EN FROM dictionary WHERE _id=?", word)
    result = cursor.fetchall()

    # conn.close()
    # cursor.close()

    return result


#
# class WordForm(Form):
#     word = StringField("Word", validators=[validators.DataRequired()])
#
#     @app.route("/", methods=["GET", "POST"])
#     def home():
#         form = WordForm(request.form)
# 		if form.validate():
# 			word = request.form["word"]
# 			result = getResult(word)[0]
# 			amh, en = result
# 			if result:
# 				result = getResult(word)[0]
# 				amh_definitions, en_grammar, en_definitions = format_result(
#                 f"{amh}\n{en}")
#
# 				return render_template(
#                 "home.html",
#                 form=form,
#                 amh_definitions=amh_definitions,
#                 en_grammar=en_grammar,
#                 en_definitions=en_definitions,
#                 word=word,
# 				)
#             else:
#                 return render_template(
#                     "home.html",
#                     form=form,
#                     error=f"No Result for {word}, Check your speeling!",
#                 )
#         else:
#             return render_template("home.html", form=form)


app = Flask(__name__)


class WordForm(Form):
    word = StringField("Word", validators=[validators.DataRequired()])


# def format_result(amh_en_text):
#     import re
#
#     parts = amh_en_text.split("n., adj., & v.")
#     amh_part = parts[0].strip()
#     en_part = "n., adj., & v." + parts[1].strip() if len(parts) > 1 else ""
#
#     amh_items = re.findall(r"\d+\s*([^0-9]+)", amh_part)
#     amh_formatted = [item.strip() for item in amh_items if item.strip()]
#
#     en_lines = en_part.split("--")
#     grammar_part = en_lines[0].strip()
#     definitions = [f"--{line.strip()}" for line in en_lines[1:]]
#
#     return amh_formatted, grammar_part, definitions
def case_correct_word(word):
    word = word.lower()
    return word[0].upper() + word[1:]


@app.route("/", methods=["GET", "POST"])
def home():
    form = WordForm(request.form)

    if form.validate():
        word = case_correct_word(request.form["word"])
        result = getResult(word)
        # print("result", result)

        if result:
            result = result[0]
            # print(result)
            amh, en = result
            # en_split = split_english_definition(en)
            #
            # # Your existing function for both sides
            # amh_definitions, en_grammar, en_definitions = format_result(f"{amh}\n{en}")
            #
            # print("SD", amh)
            # print("\nEN Parts:", en_split)

            # amh_definitions, en_grammar, en_definitions = format_result(f"{amh}\n{en}")
            # print("SD", amh)
            # print("\n")
            # print("EN:", en)

            return render_template(
                "home.html",
                form=form,
                amh=amh,
                # en_grammar=en_grammar,
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
        return render_template("home.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
