import datetime

from flask import Flask, redirect, url_for, request, flash, session, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


########################### MODELS ###########################

# http://flask-sqlalchemy.pocoo.org/2.3/models/
class User(db.Model):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True)

	user_type = db.Column(db.String(100))
	name = db.Column(db.String(100), nullable=False)
	surname = db.Column(db.String(100), nullable=False)

	username = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)

	register_date = db.Column(db.DateTime)
	last_login_date = db.Column(db.DateTime)

	recipes = db.relationship("Recipe", backref="recipes_of_user")


	def __init__(self, name, surname, username, password, email):
		self.name = name
		self.surname = surname
		self.username = username
		self.password = password
		self.email = email

		self.register_date = datetime.datetime.now()
		self.last_login_date = datetime.datetime.now()

	@staticmethod
	def get_user_by_user_name(username):
		user = User.query.filter_by(username=username).first()
		return user


class RecipeCategory(db.Model):
	__tablename__ = 'RecipeCategory'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))

	recipes = db.relationship("Recipe", backref="recipes_of_category")

	@staticmethod
	def list_of_categories():
		category_names = RecipeCategory.query(RecipeCategory.name).all()
		return category_names

class Recipe(db.Model):
	__tablename__ = 'Recipe'
	id = db.Column(db.Integer, primary_key = True)

	name = db.Column(db.String(100))
	text = db.Column(db.Text)

	category_id = db.Column(db.Integer, db.ForeignKey('RecipeCategory.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

	add_date = db.Column(db.DateTime)
	last_edit_date = db.Column(db.DateTime)

	def __init__(self, name, text, category_id, user_id, date=None):
		self.name = name
		self.text = text
		self.category_id = category_id
		self.user_id = user_id

		if date is None:
			date = datetime.datetime.now()
		self.add_date = date
		self.last_edit_date = date

	def get_ingredients(self):
		ingredient_ids = RecipeCategory.query(RecipeCategory.ingredient_id).filter_by(recipe_id=self.id)
		ingredients = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
		return ingredients

	def get_category(self):
		return RecipeCategory.query(RecipeCategory.name).filter_by(id=self.id).first()


class Ingredient(db.Model):
	__tablename__ = 'Ingredient'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	similar = db.Column(db.String(50))

	@staticmethod
	def list_of_ingredients():
		ingredients = Ingredient.query(Ingredient.name).all()
		return ingredients

	@staticmethod
	def get_similar_ingredient(name):
		similar_ingredient = Ingredient.query(Ingredient.similar).filter_by(name=name)
		return similar_ingredient


class RecipeIngredientTable(db.Model):
	__tablename__ = 'RecipeIngredientTable'
	id = db.Column(db.Integer, primary_key = True)

	# One-to-Many
	recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), nullable=False)
	# One-to-Many
	ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), nullable=False)


	def __init__(self, recipe_id, ingredient_id):
		self.recipe_id = recipe_id
		self.ingredient_id = ingredient_id


	@staticmethod
	def ingredients_for_recipe(recipe_id):
		ingredients_for_recipe = RecipeCategory.query(RecipeCategory.ingredient_id).filter_by(recipe_id=recipe_id)
		return ingredients_for_recipe

	@staticmethod
	def recipes_that_have_ingredient(ingredient_id):
		recipes_that_have_ingredient = RecipeCategory.query(RecipeCategory.recipe_id).filter_by(ingredient_id=ingredient_id)
		return recipes_that_have_ingredient





############# OTHER METHODS ##############

def check_if_user_logged_in():
	if not "logged_in" in session:
		user_logged_in = False
		session["logged_in"] = False
	else:
		user_logged_in = session["logged_in"]

	return user_logged_in


def get_datetime_by_str(datetime_string, format="%Y-%m-%d %H:%M:%S.%f"):
	return datetime.strptime(datetime_string, format)



############################### ROUTES ############################

@app.route('/', methods=['POST', 'GET'])
def home():
	if not "logged_in" in session:
		user_logged_in = False
		session["logged_in"] = False
	else:
		user_logged_in = session["logged_in"]

	if not user_logged_in:
		return render_template('log_in.html')

	if "username" in session:
		username = session["username"]
	else:
		username = ""

	recipes = Recipe.query.all()
	#print(session)

	return render_template('index.html', user_logged_in=user_logged_in, username=username, recipes=recipes)


@app.route('/log_out', methods=['POST', 'GET'])
def log_out():
	session["logged_in"] = False
	return redirect(url_for('home'))


@app.route('/log_in', methods=['POST', 'GET'])
def log_in():
	return render_template('log_in.html')


@app.route('/log_in_confirm', methods=['POST', 'GET'])
def log_in_confirm():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")

		fields = ["username", "password"]
		control = [bool(username), bool(password)]

		missing_inputs = [fields[i] for i in range(len(fields)) if not control[i]]

		if len(missing_inputs) > 0:  # check if all the fields are filled
			flash("{} field(s) must be filled!".format(missing_inputs), "error")
			print("{} field(s) must be filled!".format(missing_inputs))
			return redirect(url_for('log_in'))
		else:
			# check database
			# firstly check if username exists in database
			user = User.query.filter_by(username=username).first() # as username is already unique, this query will return at most 1 user

			if user is None:
				flash("username not found!", "error")
				print("username not found!")
				return redirect(url_for('log_in'))

			# now check if password is true
			if password != user.password:
				flash("wrong password!", "error")
				print("wrong password!")
				return redirect(url_for('log_in'))

			session["logged_in"] = True
			session["username"] = user.username
			session["user_id"] = user.id
			print("{}, logged in".format(user))
			flash("Welcome back!")
			return redirect(url_for('home'))
	else:
		print("GET, log_in_confirm")
		return redirect(url_for('log_in'))


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
			new_user = User(name=name, surname=surname, username=username, password=password, email=email)
			db.session.add(new_user)
			db.session.commit()


			session["logged_in"] = True
			session["username"] = new_user.username
			#session["user"] = new_user
			return redirect(url_for('home'))
	else:
		print("here is get")
		return redirect(url_for('sign_up'))


@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
	if not check_if_user_logged_in():
		print("You must log in!")
		flash("You must log in!", "error")
		return redirect(url_for('log_in'))
	else:
		categories = RecipeCategory.query.all()
		ingredients = Ingredient.query.all()

		return render_template('add_recipe.html', categories=categories, ingredients=ingredients)


@app.route('/add_recipe_confirm', methods=['POST', 'GET'])
def add_recipe_confirm():
	if request.method == "POST":
		recipe_name = request.form.get("recipe_name")
		recipe_text = request.form.get("recipe_text")
		category_id = request.form.get("category")
		ingredient_ids = request.form.get("ingredient")

		fields = ["recipe_name", "recipe_text", "category", "ingredient_ids"]
		control = [bool(recipe_name), bool(recipe_text), bool(category_id), bool(ingredient_ids)]

		missing_inputs = [fields[i] for i in range(len(fields)) if not control[i]]

		if len(missing_inputs) > 0:  # check if all the fields are filled
			flash("{} field(s) must be filled!".format(missing_inputs), "error")
			print("{} field(s) must be filled!".format(missing_inputs))
			return redirect(url_for('add_recipe'))
		else:
			user_id = session["user_id"]

			new_recipe = Recipe(name=recipe_name, text=recipe_text, category_id=category_id, user_id=user_id)
			db.session.add(new_recipe)
			db.session.flush()  # to get id of the recipe, changes should be committed (flushed)

			recipe_id = new_recipe.id

			for ingredient_id in ingredient_ids:
				new_recipe_ingredient = RecipeIngredientTable(recipe_id=recipe_id, ingredient_id=ingredient_id)
				db.session.add(new_recipe_ingredient)

			db.session.commit()

			print("Recipe Added!")
			flash("Recipe Added!")
			return redirect(url_for('home'))
	else:
		print("GET, add_recipe")
		return redirect(url_for('add_recipe'))



if __name__ == '__main__':
	#db.create_all()
	app.run(debug=True)
