from flask import Flask, render_template, request
from wtforms import Form, StringField, validators
import sqlite3


app = Flask(__name__)

def getResult(word):
	conn = sqlite3.connect('ahun.sqlite')
	cursor = conn.cursor()

	word = (str(word), )
	cursor.execute("SELECT AMH, EN FROM dictionary WHERE _id=?", word)
	result = cursor.fetchall()

	# conn.close()
	# cursor.close()

	return result

class WordForm(Form):
	word = StringField('Word', validators=[validators.DataRequired()])

	@app.route("/", methods=['GET', 'POST'])
	def home():
		form = WordForm(request.form)

		if form.validate():
			word = request.form["word"]

			result = getResult(word)

			if result:
				result  = getResult(word)[0]

				amh = result[0]
				en = result[1]

				return render_template('home.html',form=form, amh=amh, en=en, word=word)
			else:
				return render_template('home.html',form=form, error=f"No Result for {word}, Check your speeling!")
		else:
			return render_template('home.html', form = form)

if __name__ == "__main__":
	app.run(debug=True)