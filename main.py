import argparse
import glob
import logging
import time
from flask import Flask
from waitress import serve

import matplotlib.pyplot as plt
import pandas as pd
from yaml import SafeLoader, load


def extract_nested_values(it):
    if isinstance(it, list):
        for sub_it in it:
            yield from extract_nested_values(sub_it)
    elif isinstance(it, dict):
        for value in it.values():
            yield from extract_nested_values(value)
    else:
        yield it


def print_ingredients(ingredients: pd.Series) -> str:
    message = '<b>Ingredients:</b>\n<ul>'
    for ingredient in ingredients[0]:
        name = list(ingredient.keys())[0]
        amounts = ingredient.values()
        unpacked = [list(extract_nested_values(amount)) for amount in amounts][0]
        unpacked = ' '.join(str(element) for element in unpacked)
        message = message + f'<li>{name}: {unpacked}</li>\n'
    message += "</ul>"
    return message


def print_steps(steps: pd.Series) -> str:
    message = '<ul>'
    message += '\n'.join(f"<li>{step['step']}</li>" for step in steps[0])
    message += '</ul>'
    return message

def print_notes(notes: pd.Series) -> str:
    if not notes:
        return ''

    notes_message = 'Note:\n- ' + '\n- '.join(notes)
    return notes_message


def reformat_yield_column(yields: pd.Series) -> str:
    """
    Convert the ORF-parsed yield data into a tuple for easier use with Pandas
    """
    drink_yield = []
    for item in yields:
        drink_yield.append(tuple(extract_nested_values(item)))
    return drink_yield


def create_ingredient_set(ingredients: pd.Series) -> pd.Series:
    """
    Convert the ORF-parsed ingredient data to a set of ingredients without amounts for easier use with Pandas
    """
    result = []
    for ingredient_set in ingredients:
        result.append({key for d in ingredient_set for key in d.keys()})
    return pd.Series(result)


def print_yield(yields: pd.Series) -> str:
    message = 'Yields '
    drink_yield = ' '.join(map(str, yields))
    message = message + drink_yield + '.'
    return message


def plot_ingredient_pie_chart(ingredients: pd.Series) -> None:
    ingredient_totals = ingredients.explode().value_counts()
    top_ingredients = ingredient_totals[ingredient_totals >= 5]  # Used in five or more recipes
    other_ingredients = pd.Series({'other': ingredient_totals[ingredient_totals < 5].sum()})
    top_ingredients = top_ingredients.append(other_ingredients)
    top_ingredients.plot.pie(rotatelabels=True)
    plt.savefig('out/top_ingredients.png')


def create_recipe_dataframe(path: str) -> pd.DataFrame:
    recipe_files = glob.glob(f'{path}/*.yml')
    df_recipes = pd.DataFrame()
    for file in recipe_files:
        with open(file) as yml_file:
            yml_contents = load(yml_file, Loader=SafeLoader)
        df_recipes = pd.concat([df_recipes, pd.json_normalize(yml_contents)], ignore_index=True)
    df_recipes.yields = reformat_yield_column(df_recipes.yields)
    df_recipes['ingredient_set'] = create_ingredient_set(df_recipes.ingredients)

    print(df_recipes)

    return df_recipes


def print_recipe_info(recipe: pd.DataFrame) -> str:
    message = '' 
    message += f'\n<h1>{recipe.recipe_name.values[0]}</h1>'
    message += f'\n{print_ingredients(recipe.ingredients.values)}'
    message += f'\n<h3>Steps:</h3>{print_steps(recipe.steps.values)}'
    message += f'\n{print_yield(recipe.yields.values[0])}'
    message += f'\n{print_notes(recipe.notes.values[0])}'

    return message

def visualize_data(recipe: pd.DataFrame) -> None:
    plot_ingredient_pie_chart(recipe.ingredient_set)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('recipe_directory', type=str)
    parser.add_argument('log_file', type=str)
    args = parser.parse_args()

    logging.basicConfig(filename=f'log/{args.log_file}', level=logging.INFO, force=True,
                        format='%(asctime)s, %(levelname)s, %(name)s, %(message)s')
    logging.info('Processing recipe data')


    df_cocktails = create_recipe_dataframe(args.recipe_directory)

    # Analyze Data
    visualize_data(df_cocktails)

    app=Flask('cocktails')
    @app.route('/drink')
    def run_code():
        start_time = time.perf_counter()
       
        output_example = df_cocktails.sample(n=1)
        html_recipe = print_recipe_info(output_example)
        print(html_recipe)
     
        end_time = time.perf_counter()
        total = end_time - start_time
        logging.info('Processing recipe data complete in %s seconds', str(total))
    
        return f"{html_recipe}"

    logging.info('Hosting cocktail data')
    serve(app, host='0.0.0.0', port=80)



if __name__ == "__main__":
    main()
