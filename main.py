from flask import Flask, request, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

def connect_to_db(db_name):
    """Connect to the SQLite database."""
    conn = sqlite3.connect(db_name)
    return conn

def get_recipes_by_ingredients(conn, ingredients):
    """
    Fetch recipes that match the given ingredients.
    
    :param conn: SQLite database connection object
    :param ingredients: List of ingredients provided by the user
    :return: DataFrame containing matching recipes
    """
    # Construct the SQL query to find recipes with any of the provided ingredients
    ingredients_like_clause = ' OR '.join([f"Ingredients LIKE '%{ingredient}%'" for ingredient in ingredients])
    query = f"SELECT * FROM recipes WHERE {ingredients_like_clause}"
    df = pd.read_sql_query(query, conn)
    return df

def format_recipe(recipe):
    """
    Format the recipe details for better readability.
    
    :param recipe: Series object containing the recipe details
    :return: Formatted string of the recipe details
    """
    formatted_recipe = """
# {title}

## Ingredients

{ingredients}

## Instructions:

{instructions}
    """.format(
        title=recipe['Title'],
        ingredients=recipe['Ingredients'].replace("[", "").replace("]", "").replace("'", "").replace(", ", "\n- "),
        instructions=recipe['Instructions']
    )
    return formatted_recipe.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    user_input = request.form['ingredients']
    ingredients = [ingredient.strip() for ingredient in user_input.split(",")]

    conn = connect_to_db("13k-recipes.db")
    matching_recipes = get_recipes_by_ingredients(conn, ingredients)
    
    if matching_recipes.empty:
        result = "No recipes found with the given ingredients."
    else:
        # Sort recipes by the number of matching ingredients
        matching_recipes['Match Count'] = matching_recipes['Ingredients'].apply(lambda x: sum(ingredient in x for ingredient in ingredients))
        best_match = matching_recipes.sort_values(by='Match Count', ascending=False).iloc[0]
        result = format_recipe(best_match)
    
    conn.close()
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
