import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'cooking_receipe_center'
app.config["MONGO_URI"] = "mongodb+srv://sagie86:na86THaN@myfirstcluster-1bh9v.mongodb.net/cooking_receipe_center?retryWrites=true&w=majority"

mongo = PyMongo(app)


# This function shows all the recipes collected
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    data = []
    for x in mongo.db.recipes.find():
        data.append(x)
    return render_template('recipes.html', recipes=data)


# This function helps to add a new recipe
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html', origin=mongo.db.origin.find(),
    categories=mongo.db.categories.find())


# This function helps to insert newly added recipe to the database
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


# this function helps to edit already inputed date from the database
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    all_origin = mongo.db.origin.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories,
                             origin=all_origin)


# This function updates the database with newly edited information
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name': request.form.get('recipe_name'),
        'origin_name': request.form.get('origin_name'),
        'category_name': request.form.get('category_name'),
        'ingredients': request.form.get('ingredients'),
        'recipe_descriptions': request.form.get('recipe_descriptions'),
        'required_tools': request.form.get('required_tools'),
        'full_name': request.form.get('full_name'),
        'email': request.form.get('email'),
        'date': request.form.get('date'),
        'i_certify': request.form.get('i_certify')
    })
    return redirect(url_for('get_recipes'))


# This function helps to delete inputed recipe from the database
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


@app.route('/tools')
def tools():
    return render_template('tools.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
       port=int(os.environ.get('PORT')),
       debug=True)
