import datetime
import numpy as np
from sklearn.cluster import KMeans
from flask import Flask, redirect, url_for, request, flash, session, render_template
from  flask_sqlalchemy import SQLAlchemy

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


	def __init__(self, user_type, name, surname, username, password, email):
		self.user_type = user_type
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

	@staticmethod
	def get_username_by_id(user_id):
		user = User.query.filter_by(id=id).first()
		return user.username


class RecipeCategory(db.Model):
	__tablename__ = 'RecipeCategory'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))

	recipes = db.relationship("Recipe", backref="recipes_of_category")

	@staticmethod
	def list_of_categories():
		category_names = RecipeCategory.query(RecipeCategory.name).all()
		return category_names

class Cluster(db.Model):
	__tablename__ = 'Cluster'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
	cluster = db.Column(db.Integer)

	def __init__(self, user_id, cluster):
		self.user_id = user_id
		self.cluster = cluster

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

	def get_score(self):
		recipe_votes = Vote.query.filter_by(recipe_id=self.id)

		score = 0
		for vote in recipe_votes:
			score += vote.value

		return score

	def get_username_by_id(self):
		user = User.query.filter_by(id=self.user_id).first()
		return user.username





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


class Vote(db.Model):
	__tablename__ = 'Vote'
	id = db.Column(db.Integer, primary_key = True)
	value = db.Column(db.Integer, nullable=False)

	# One-to-Many
	recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'), nullable=False)
	# One-to-Many
	user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


	def __init__(self, recipe_id, user_id, value):
		self.recipe_id = recipe_id
		self.user_id = user_id
		self.value = value



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

def createCluster():
	all_users = User.query.filter_by()
	all_ingredients = RecipeCategory.query.filter_by()
	user_count = 0
	ingredient_count = 0
	for user in all_users:
		user_count += 1
	for ingredient in all_ingredients:
		ingredient_count += 1
	user_array = np.zeros((user_count,1) , dtype = 'int32')
	ingredient_array = np.zeros((user_count,ingredient_count),dtype='float64')

	for i in range(user_count):
		all_votes = Vote.query.filter_by(user_id = i)
		for vote in all_votes:
			all_liked_recipes = RecipeIngredientTable.query.filter_by(recipe_id = vote.recipe_id)
			for liked_recipe in all_liked_recipes:
				if(liked_recipe.ingredient_id >= 0 and liked_recipe.ingredient_id < ingredient_count):
					ingredient_array[i,liked_recipe.ingredient_id]+=1

	user_clusters = KMeans(n_clusters=5).fit_predict(ingredient_array)
	return user_clusters



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

	username = session["username"]
	user_id = session["user_id"]
	session["url"] = "/"

	recipes = Recipe.query.all()
	already_voted_recipes = Vote.query.filter_by(user_id=user_id)
	already_voted_recipe_ids = [vote.recipe_id for vote in already_voted_recipes]

	return render_template('index.html', user_logged_in=user_logged_in,
	                       username=username, user_id=user_id, recipes=recipes,
	                       already_voted_recipes=already_voted_recipes, already_voted_recipe_ids=already_voted_recipe_ids)


@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
	if not "logged_in" in session:
		user_logged_in = False
		session["logged_in"] = False
	else:
		user_logged_in = session["logged_in"]

	if not user_logged_in:
		return render_template('log_in.html')

	username = session["username"]
	user_id = session["user_id"]
	session["url"] = "/"


	recipes = []
	user_type = Cluster.query.filter_by(user_id = user_id).first()
	similar_users = Cluster.query.filter_by(cluster=user_type.cluster).all()
	for similar_user in similar_users:
		recipe_username_pairs = Recipe.query.filter_by(user_id=similar_user.user_id).all()
		for recipe_username_pair in recipe_username_pairs:
			recipe = Recipe.query.filter_by(id = recipe_username_pair.id)
			recipes.append(recipe)

	already_voted_recipes = Vote.query.filter_by(user_id=user_id)
	already_voted_recipe_ids = [vote.recipe_id for vote in already_voted_recipes]


	return render_template('recommend.html', user_logged_in=user_logged_in,
	                       username=username, user_id=user_id, recipes=recipes,
	                       already_voted_recipes=already_voted_recipes, already_voted_recipe_ids=already_voted_recipe_ids)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
	if check_if_user_logged_in():
		user_id = session["user_id"]

		recipes = Recipe.query.filter_by(user_id=user_id)

		return render_template('profile.html', username=session["username"], recipes=recipes)
	else:
		return render_template('log_in.html')


################admin and verificate
@app.route('/admin', methods=['POST', 'GET'])
def admin():
	if not "logged_in" in session:
		user_logged_in = False
		session["logged_in"] = False
	else:
		user_logged_in = session["logged_in"]

	if not user_logged_in:
		return render_template('log_in.html')

	if not session["username"] == "admin":
		return redirect(url_for('home'))


	users = User.query.all()
	return render_template('admin.html', user_logged_in=user_logged_in, username='admin', users = users)

@app.route("/verificate/<string:uname>",  methods = ["GET"])
def verify(uname):
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
	user = User.query.filter_by(username=uname).first()
	if user.user_type == 'verified':
		user.user_type = 'nonverified'

	else:
		user.user_type = 'verified'
	db.session.commit()

	return redirect(url_for('admin'))

########################

@app.route('/log_out', methods=['POST', 'GET'])
def log_out():
	session["logged_in"] = False
	return redirect(url_for('home'))


@app.route('/log_in', methods=['POST', 'GET'])
def log_in():
	user_clusters = createCluster()
	#clusters = Cluster.query.all()
	#for cluster in clusters:
		#db.session.delete(cluster)
	for i in range(len(user_clusters)):
		print(str(i) + ' ' + str(user_clusters[i]))
		user_profile = Cluster(user_id = i, cluster=user_clusters[i])
		try:
			db.session.add(user_profile)
			print(str(i) + ' ' + str(user_clusters[i]))
			db.session.flush()
			print(str(i) + ' ' + str(user_clusters[i]))
			db.session.commit()
			print(str(i) + ' ' + str(user_clusters[i]))
		except:
			print('X')
			continue
	try:
		db.session.commit()
	except:
		print('Already exists')

	return render_template('log_in.html')


@app.route('/log_in_confirm', methods=['POST', 'GET'])
def log_in_confirm():
	print('try')
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
			if user.username == "admin":
				return redirect(url_for('admin'))
			else:
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

		email_already = User.query.filter_by(email=email).first()
		email_already_cond = (email_already) is None
		user_already = User.query.filter_by(username=username).first()
		user_already_cond = (user_already) is None
		password = request.form.get("pass")
		password_re = request.form.get("re_pass")
		user_type = 'nonverified'
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
		elif email_already_cond == False:
			flash("Email is already taken!", "error")
			print("Email is already taken!")
			return redirect(url_for('sign_up'))
		elif user_already_cond == False:
			flash("User is already taken!", "error")
			print("User is already taken!")
			return redirect(url_for('sign_up'))
		else:
			# add user into database
			new_user = User(user_type = user_type,name=name, surname=surname, username=username, password=password, email=email)
			db.session.add(new_user)
			db.session.flush()

			user_id = new_user.id
			db.session.commit()


			session["logged_in"] = True
			session["username"] = new_user.username
			session["user_id"] = new_user.id
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
		ingredient_ids = request.form.getlist("ingredient")
		print(category_id)
		print(category_id)
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

			print("ingredient_ids = {}".format(ingredient_ids))
			print(type(ingredient_ids))
			for ingredient_id in ingredient_ids:
				new_recipe_ingredient = RecipeIngredientTable(recipe_id=recipe_id, ingredient_id=ingredient_id)
				db.session.add(new_recipe_ingredient)
				db.session.flush()

			db.session.commit()

			print("Recipe Added!")
			flash("Recipe Added!")
			return redirect(url_for('home'))
	else:
		print("GET, add_recipe")
		return redirect(url_for('add_recipe'))


@app.route('/edit_recipe/<string:recipe_id>', methods=['POST', 'GET'])
def edit_recipe(recipe_id):
	if not check_if_user_logged_in():
		print("You must log in!")
		flash("You must log in!", "error")
		return redirect(url_for('log_in'))
	else:
		#categories = RecipeCategory.query.all()
		#ingredients = Ingredient.query.all()
		recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()

		if "user_id" in session:
			user_id = session["user_id"]
		else:
			username = session["username"]
			user = User.query.filter_by(username=username).first()
			user_id = user.id

		if not recipe.user_id == user_id:
			print("You are not authorized to edit this recipe")
			flash("You are not authorized to edit this recipe", "error")
			return redirect(url_for('home'))
		else:
			session["recipe_id"] = recipe_id
			return render_template('edit_recipe.html', recipe=recipe)


@app.route('/edit_recipe_confirm', methods=['POST', 'GET'])
def edit_recipe_confirm():
	if not "recipe_id" in session:
		return redirect(url_for('home'))
	else:
		recipe_id = session["recipe_id"]

	if request.method == "POST":
		recipe_name = request.form.get("recipe_name")
		recipe_text = request.form.get("recipe_text")
		#category_id = request.form.get("category")
		#ingredient_ids = request.form.get("ingredient")

		fields = ["recipe_name", "recipe_text"]
		control = [bool(recipe_name), bool(recipe_text)]

		missing_inputs = [fields[i] for i in range(len(fields)) if not control[i]]

		if len(missing_inputs) > 0:  # check if all the fields are filled
			flash("{} field(s) must be filled!".format(missing_inputs), "error")
			print("{} field(s) must be filled!".format(missing_inputs))
			return redirect('edit_recipe/{}'.format(recipe_id))
		else:
			recipe = Recipe.query.get(recipe_id)
			recipe.name = recipe_name
			recipe.text = recipe_text
			recipe.last_edit_date = datetime.datetime.now()

			db.session.commit()
			del session["recipe_id"]

			print("Recipe Edited!")
			flash("Recipe Edited!")
			return redirect(url_for('home'))
	else:
		print("GET, edit_recipe")
		return redirect('edit_recipe/{}'.format(recipe_id))


@app.route('/delete_recipe/<string:recipe_id>', methods=['POST', 'GET'])
def delete_recipe(recipe_id):
	if not check_if_user_logged_in():
		print("You must log in!")
		flash("You must log in!", "error")
		return redirect(url_for('log_in'))
	else:
		#categories = RecipeCategory.query.all()
		#ingredients = Ingredient.query.all()
		recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()

		if "user_id" in session:
			user_id = session["user_id"]
		else:
			username = session["username"]
			user = User.query.filter_by(username=username).first()
			user_id = user.id

		if not recipe.user_id == user_id:
			print("You are not authorized to delete this recipe")
			flash("You are not authorized to delete this recipe", "error")
			return redirect(url_for('home'))
		else:
			session["recipe_id"] = recipe_id
			return render_template('delete_recipe.html', recipe=recipe)


@app.route('/delete_recipe_confirm', methods=['POST', 'GET'])
def delete_recipe_confirm():
	if not "recipe_id" in session:
		return redirect(url_for('home'))
	else:
		recipe_id = session["recipe_id"]

	if request.method == "POST":
		choice = request.form.get("confirmation")

		fields = ["choice"]
		control = [bool(choice)]

		missing_inputs = [fields[i] for i in range(len(fields)) if not control[i]]

		if len(missing_inputs) > 0:  # check if all the fields are filled
			flash("{} field(s) must be filled!".format(missing_inputs), "error")
			print("{} field(s) must be filled!".format(missing_inputs))
			return redirect('edit_recipe/{}'.format(recipe_id))
		else:
			if choice == "yes":
				recipe = Recipe.query.get(recipe_id)

				# delete foreign keys
				recipe_ingredients = RecipeIngredientTable.query.filter_by(recipe_id=recipe_id)
				print("recipe_ingredients = {}".format(recipe_ingredients))
				for recipe_ingredient in recipe_ingredients:
					db.session.delete(recipe_ingredient)
				# then delete itself
				db.session.delete(recipe)
				db.session.commit()

				print("Recipe Deleted!")
				flash("Recipe Deleted!")
				del session["recipe_id"]
				return redirect(url_for('home'))
			else:
				print("You are not sure to delete the recipe!")
				return redirect(url_for('home'))
	else:
		print("GET, delete_recipe")
		return redirect('delete_recipe/{}'.format(recipe_id))


@app.route('/vote_recipe/<string:recipe_id>/<string:evaluation>', methods=['POST', 'GET'])
def vote_recipe(recipe_id, evaluation):
	#if request.method == "POST":
		if not check_if_user_logged_in():
			print("You must log in to vote")
			flash("You must log in to vote", "error")
			return redirect(url_for('home'))

		# check if recipe_id is valid
		recipe_query = Recipe.query.filter_by(id=recipe_id)
		recipe_count = recipe_query.count()
		if  recipe_count == 0:
			print("There is no such recipe")
			flash("There is no such recipe", "error")
			return redirect(url_for('home'))

		recipe = recipe_query.first()

		# check if user has already voted that recipe
		user_id = session["user_id"]
		if Vote.query.filter_by(recipe_id=recipe_id, user_id=user_id).count() > 0:
			print("You have already voted to that recipe")
			flash("You have already voted to that recipe", "error")
			return redirect(url_for("home"))


		# check if user is not owning the recipe
		if recipe.user_id == user_id:
			print("You cannot vote your own recipe")
			flash("You cannot vote your own recipe", "error")
			return redirect(url_for("home"))

		if evaluation == "like":
			value = 1
		elif evaluation == "dislike":
			value = -1
		else:
			print("Invalid evaluation")
			flash("Invalid evaluation", "error")
			return redirect(url_for("home"))

		# check if user is a verified chef or not
		user = User.query.get(user_id)
		if user.user_type == "verified":
			value *= 3

		new_vote = Vote(user_id=user_id, recipe_id=recipe_id, value=value)
		db.session.add(new_vote)
		db.session.commit()
		return redirect(url_for("home"))

	#else:
	#	print("GET, vote_recipe")
	#	return redirect(url_for('home'))

@app.route('/search', methods=['POST', 'GET'])
def search():

	if not check_if_user_logged_in():
		return redirect(url_for('home'))

	session["url"] = "search"

	if request.method == "POST":  # result of search
		print("POST, search")
		search_text = request.form.get("search_text")
		search_by = request.form.get("search_by")
		#ingredient_ids = request.form.get("ingredient")

		fields = ["search_text", "search_by"]
		control = [bool(search_text), bool(search_by)]

		missing_inputs = [fields[i] for i in range(len(fields)) if not control[i]]

		if len(missing_inputs) > 0:  # check if all the fields are filled
			flash("{} field(s) must be filled!".format(missing_inputs), "error")
			print("{} field(s) must be filled!".format(missing_inputs))
			return render_template('search.html', method="GET")
		else:
			user_id = session["user_id"]
			recipes = Recipe.query.all()
			already_voted_recipes = Vote.query.filter_by(user_id=user_id)
			already_voted_recipe_ids = [vote.recipe_id for vote in already_voted_recipes]

			# implement search logic here
			if search_by == "ingredient":

				ingredients = search_text
				selected_ingredient = Ingredient.query.filter_by(name=ingredients).first()
				if(((selected_ingredient) is None)):
					return render_template('search.html', method="GET")
				recipe_ingredient_pairs = RecipeIngredientTable.query.filter_by(ingredient_id=selected_ingredient.id)

				recipes=[]
				for recipe_ingredient_pair in recipe_ingredient_pairs:
					recipe = Recipe.query.filter_by(id = recipe_ingredient_pair.recipe_id)
					recipes.append(recipe)

				print(recipes)
				return render_template('search.html', method="POST", recipes=recipes, user_id=user_id, already_voted_recipe_ids=already_voted_recipe_ids)
			elif search_by == "recipe_name":
				recs = "%" +search_text+ "%"

				selected_rec = Recipe.query.filter(Recipe.name.like(recs)).all()
				if(((selected_rec) is None)):
					return render_template('search.html', method="GET")
				recipes=[]
				for rec in selected_rec:
					recipe = Recipe.query.filter_by(id = rec.id)
					recipes.append(recipe)
				return render_template('search.html', method="POST", recipes=recipes, user_id=user_id, already_voted_recipe_ids=already_voted_recipe_ids)
			elif search_by == "recipe_text":
				recs = "%" +search_text+ "%"

				selected_rec = Recipe.query.filter(Recipe.text.like(recs)).all()
				if(((selected_rec) is None)):
					return render_template('search.html', method="GET")
				recipes=[]
				for rec in selected_rec:
					recipe = Recipe.query.filter_by(id = rec.id)
					recipes.append(recipe)
				return render_template('search.html', method="POST", recipes=recipes, user_id=user_id, already_voted_recipe_ids=already_voted_recipe_ids)

			elif search_by == "user_name":
				user_name = search_text
				recipes = []
				selected_username = User.query.filter_by(username=user_name).first()
				if(((selected_username) is None)):
					return render_template('search.html', method="GET")

				recipe_username_pairs = Recipe.query.filter_by(user_id=selected_username.id).all()
				if(((recipe_username_pairs) is None)):
					return render_template('search.html', method="GET")

				for recipe_username_pair in recipe_username_pairs:
					recipe = Recipe.query.filter_by(id = recipe_username_pair.id)
					recipes.append(recipe)
				print(recipes)
				return render_template('search.html', method="POST", recipes=recipes, user_id=user_id, already_voted_recipe_ids=already_voted_recipe_ids)
			else:
				# error
				render_template('search.html', method="GET")

			render_template('search.html', method="GET")
	else:  # prompt user to search
		print("GET, search")
		return render_template('search.html', method="GET")


@app.route('/leaderboard', methods=['POST', 'GET'])
def leaderboard():
	if not "logged_in" in session:
		user_logged_in = False
		session["logged_in"] = False
	else:
		user_logged_in = session["logged_in"]

	if not user_logged_in:
		return render_template('log_in.html')

	username = session["username"]
	user_id = session["user_id"]
	session["url"] = "leaderboard"

	recipes = Recipe.query.all()
	sorted_recipes = sorted(recipes, key=lambda x: x.get_score(), reverse=True)

	sorted_recipes = sorted_recipes[:10]

	already_voted_recipes = Vote.query.filter_by(user_id=user_id)
	already_voted_recipe_ids = [vote.recipe_id for vote in already_voted_recipes]
	#print("already_voted_recipe_ids", already_voted_recipe_ids)
	#print(session)

	return render_template('leaderboard.html',
	                       username=username, user_id=user_id, recipes=sorted_recipes,
	                       already_voted_recipe_ids=already_voted_recipe_ids)

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
