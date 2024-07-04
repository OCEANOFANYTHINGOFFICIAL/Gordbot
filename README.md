# Gordbot

<p align="center">
    <img src="https://img.shields.io/badge/license-GNU%20GPLv3.0-blue" alt="GitHub license">
    <img src="https://img.shields.io/github/issues/OCEANOFANYTHINGOFFICIAL/Gordbot" alt="GitHub issues">
    <img src="https://img.shields.io/github/stars/OCEANOFANYTHINGOFFICIAL/Gordbot" alt="GitHub stars">
    <img src="https://img.shields.io/github/forks/OCEANOFANYTHINGOFFICIAL/Gordbot" alt="GitHub forks">
    <img src="https://img.shields.io/github/last-commit/OCEANOFANYTHINGOFFICIAL/Gordbot" alt="GitHub last commit">
    <img src="https://img.shields.io/badge/python-3.6%2B-blue" alt="Python version">
    <img src="https://img.shields.io/badge/flask-2.0.0-green" alt="Flask version">
    <img src="https://img.shields.io/badge/pandas-1.2.0-red" alt="Pandas version">
</p>

Welcome to **Gordbot**! This AI project is designed to generate detailed recipes based on user-provided ingredients. The project is implemented in Python and utilizes two main modules: `pandas` for data processing and `flask` for the web UI.

## Installation

To get started with Gordbot, follow these steps:

### Clone the Repository

```sh
git clone https://github.com/OCEANOFANYTHINGOFFICIAL/Gordbot.git
cd Gordbot
```

### Install Requirements

First, make sure you have Python installed. Then, install the required packages using `pip`:

```sh
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the following command:

```sh
python main.py
```

This will start the Flask web server. Open your web browser and go to `http://127.0.0.1:5000/` to interact with Gordbot.

## Main Modules

### pandas

`pandas` is used for data processing within the application. It helps in reading the SQLite database and manipulating data frames.

### flask

`flask` is used for creating the web UI of the application. It handles the routing and rendering of HTML templates.

## Database

This project uses a dataset file `13k-recipes.db` from the repo: [Joseph R Martinez - Recipe Dataset](https://github.com/josephrmartinez/recipe-dataset). A big shoutout for providing such a comprehensive dataset!

## Code Overview

```python
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
        matching_recipes['Match Count'] = matching_recipes['Ingredients'].apply(lambda x: sum(ingredient in x for ingredient in ingredients))
        best_match = matching_recipes.sort_values(by='Match Count', ascending=False).iloc[0]
        result = format_recipe(best_match)
    
    conn.close()
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
```

## Contributing

Contributions are welcome! If you want to contribute to Gordbot, follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix:

    ```sh
    git checkout -b my-new-feature
    ```

3. Make your changes and commit them:

    ```sh
    git commit -am 'Add new feature'
    ```

4. Push to the branch:

    ```sh
    git push origin my-new-feature
    ```

5. Create a new Pull Request.

## License

This project is licensed under GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
