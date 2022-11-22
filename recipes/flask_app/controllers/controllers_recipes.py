from flask_app import app
from flask import render_template, redirect, session, flash, request
from flask_app.models.models_user import User
from flask_app.models.models_recipe import Recipe
from flask_app.config.mysqlconnection import connectToMySQL

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    all = Recipe.all_recipes()
    return render_template("dashboard.html", user = user, all = all)

# Create a new recipe page
@app.route('/add_recipe')
def add_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

# Create Recipe adds to db
@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_cooked' : request.form['date_cooked'],
        'under_thirty' : request.form['under_thirty'],
        'user_id' : session['user_id'],
    }
    Recipe.create_recipe(data)
    return redirect('/dashboard')

# Display One Recipe
@app.route('/show_recipe/<int:recipe_id>')
def show_recipe(recipe_id):
    data = {
        'id' : recipe_id
    }
    recipe = Recipe.get_one(data)
    return render_template('one_recipe.html', recipe = recipe)

# Edit Recipe
@app.route('/edit_recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        'id' : recipe_id
    }
    recipe= Recipe.get_one(data)
    return render_template('edit_recipe.html', recipe = recipe)

# Update one recipe
@app.route('/update_recipe/<int:recipe_id>', methods = ['POST'])
def update_recipe(recipe_id):
    Recipe.update_recipe(request.form, recipe_id)
    return redirect('/dashboard')

# delete a recipe
@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    data = {
        'id' : recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')