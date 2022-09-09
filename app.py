from flask import Flask, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
from passlib.handlers.sha2_crypt import sha256_crypt
from wtforms import Form, StringField, validators, PasswordField

from article_data import Articles

app = Flask(__name__)

Articles = Articles()

# Config MySQL DB
app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'Tomodachi@2001'
app.config["MYSQL_DB"] = 'flask_blog_app'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

mysql = MySQL(app)


class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=5, max=40)])
	username = StringField('Username', [validators.Length(min=7, max=30)])
	email = StringField('Email', [validators.Length(min=7, max=35)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message="Password does not match")
	])
	confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', "POST"])
def register():
	form = RegisterForm(request.form)
	if request.method == "POST" and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.hash(str(form.password.data))

		# Creates cursor
		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
		mysql.connection.commit()

		cur.close()

		flash('You are now registered and may login. Welcome to BlogIt!', 'success')

		redirect(url_for('articles'))

	return render_template('register.html', form=form)


@app.route('/')
def home():  # put application's code here
	return render_template("home.html")


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/articles')
def articles():
	return render_template('articles.html', articles=Articles)


@app.route('/articles/<string:id>/')
def display_article(id):
	return render_template('article.html', id=id)


if __name__ == '__main__':
	app.run(debug=True)

app.secret_key = 'Secret145'
