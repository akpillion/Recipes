from flask_app.models.models_user import User
from flask_app.config.mysqlconnection import connectToMySQL

db = "recipes_db"

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None

# Create Recipe
    @classmethod
    def create_recipe(cls, data):
        query = """
                INSERT INTO recipes (name, description, instructions, date_cooked, under_thirty, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_thirty)s, %(user_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

# Display recipes
    @classmethod
    def all_recipes(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

# Display One Recipe
    # @classmethod
    # def get_one(cls, data):
    #     query = """
    #             SELECT * FROM recipes
    #             WHERE id = %(id)s
    #             """
    #     results = connectToMySQL(db).query_db(query, data)
    #     return cls(results[0])

# one to many relationship
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM recipes
                JOIN users ON users.id = recipes.user_id
                WHERE recipes.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        recipe = cls(results[0])
        owner_data = {
            'id' : results[0]['id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['created_at'],
            'updated_at' : results[0]['updated_at']
        }
        recipe.owner = User(owner_data)
        return recipe

    @classmethod
    def update_recipe(cls, form_data, recipe_id):
        query = f"UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, under_thirty = %(under_thirty)s, WHERE id = {recipe_id}"
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def delete_recipe(cls, data):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s
                """
        return connectToMySQL(db).query_db(query, data)