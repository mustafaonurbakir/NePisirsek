import datetime

from flask import Flask, redirect, url_for, request, flash, session, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)

	user_type = db.Column(db.String(100))
	name = db.Column(db.String(100))
	surname = db.Column(db.String(100))
	username = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))

	register_date = db.Column(db.String(100))
	last_login_date = db.Column(db.String(100))

	def __init__(self, name, surname, username, password):
		self.name = name
		self.surname = surname
		self.username = username
		self.password = password
		self.register_date = datetime.datetime.now()
		self.last_login_date = datetime.datetime.now()


@app.route('/', methods=['POST', 'GET'])
def home():
	if not "logged_in" in session:
		user_logged_in = False
	else:
		user_logged_in = session["logged_in"]
	return render_template('index.html', user_logged_in=user_logged_in)

@app.route('/log_out', methods=['POST', 'GET'])
def log_out():
	session["logged_in"] = False
	return redirect(url_for('home'))

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
	return render_template('sign_in.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
	return render_template('sign_up.html')

@app.route('/sign_up_confirm', methods=['POST', 'GET'])
def sign_up_confirm():
	if request.method == "POST":
		name = request.form.get("name")
		surname = request.form.get("your_surname")
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("pass")
		password_re = request.form.get("re_pass")

		fields = ["name", "surname", "username", "email", "password"]
		control = [bool(name), bool(surname), bool(username), bool(email), bool(password), bool(password_re)]

		missing_inputs = [fields[i] for i in range(len(fields)) if not control[i]]

		if len(missing_inputs) > 0:  # check if all the fields are filled
			flash("{} field(s) must be filled!".format(missing_inputs), "error")
			print("{} field(s) must be filled!".format(missing_inputs))
			return redirect(url_for('sign_up'))
		elif password != password_re:
			flash("passwords do not match!", "error")
			print("passwords do not match!")
			return redirect(url_for('sign_up'))
		else:
			# add user into database
			new_user = User(name=name, surname=surname, username=username, password=password)
			db.session.add(new_user)
			db.session.commit()


			session["logged_in"] = True
			#session["user"] = new_user
			print("successful")
			return redirect(url_for('home'))
	else:
		print("here is get")
		return redirect(url_for('sign_up'))


if __name__ == '__main__':
	#db.create_all()
	app.run(debug=True)
