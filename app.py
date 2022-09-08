from flask import Flask, render_template, request
from wtforms import Form, StringField, validators, PasswordField

from article_data import Articles

app = Flask(__name__)

Articles = Articles()


class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=5, max=40)])
	username = StringField('Username', [validators.Length(min=7, max=30)])
	email = StringField('Email', [validators.Length(min=7, max=35)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message="Password does not match")
	])
	confirm = PasswordField('Confirm Password')


@app.route('/register', methods =['GET', "POST"])
def register():
	form = RegisterForm(request.form)
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
