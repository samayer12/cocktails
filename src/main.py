"""Ingest cocktail data from .yml files and host as simple endpoints"""

import argparse
import glob
import logging
import time
import matplotlib.pyplot as plt
import pandas as pd
import yaml.composer
import yaml.parser
import yaml.scanner

from flask import Flask
from yaml import SafeLoader, load
from waitress import serve
from printer import print_recipe_info
from util import create_directories, reformat_yield_column, create_ingredient_set


def create_recipe_dataframe(path: str) -> pd.DataFrame:
    """Read ORF-compliant (unvalidated) .yml files and store them in a dataframe"""
    recipe_files = glob.glob(f'{path}/*.yml')
    df_recipes = pd.DataFrame()
    for file in recipe_files:
        with open(file, encoding='UTF-8') as yml_file:
            try:
                yml_contents = load(yml_file, Loader=SafeLoader)
            except yaml.scanner.ScannerError:
                logging.error('Bad YAML scan in %s', str(file))
            except yaml.parser.ParserError:
                logging.error('Bad YAML parse in %s', str(file))
            except yaml.composer.ComposerError:
                logging.error('Bad YAML compose in %s', str(file))
        df_recipes = pd.concat([df_recipes, pd.json_normalize(yml_contents)], ignore_index=True)
    df_recipes.yields = reformat_yield_column(df_recipes.yields)
    df_recipes['ingredient_set'] = create_ingredient_set(df_recipes.ingredients)

    print(df_recipes)

    return df_recipes


def plot_ingredient_pie_chart(ingredients: pd.Series) -> None:
    """
    Create a pie chart of all ingredients that appear in N or more recipes.
    Currently hardcoded.
    """
    ingredient_totals = ingredients.explode().value_counts()
    top_ingredients = ingredient_totals[ingredient_totals >= 5]  # Used in five or more recipes
    other_ingredients = pd.Series({'other': ingredient_totals[ingredient_totals < 5].sum()})
    top_ingredients = top_ingredients.append(other_ingredients)
    top_ingredients.plot.pie(rotatelabels=True)
    plt.savefig('out/top_ingredients.png')


def visualize_data(recipe: pd.DataFrame) -> None:
    """Place all dataviz calls here"""
    plot_ingredient_pie_chart(recipe.ingredient_set)


def main():
    """Here's where the magic happens. Kinda kludgy, should consider other website-hosting means."""
    parser = argparse.ArgumentParser()
    parser.add_argument('recipe_directory', type=str)
    parser.add_argument('log_file', type=str)
    args = parser.parse_args()

    create_directories(['out', 'log'])

    logging.basicConfig(filename=f'log/{args.log_file}', level=logging.DEBUG, force=True,
                        format='%(asctime)s, %(levelname)s, %(name)s, %(message)s')

    logging.info('Processing recipe data.')
    df_cocktails = create_recipe_dataframe(f"{args.recipe_directory}/girly_drinks/")
    logging.info('Recipe data ingest complete.')

    logging.info('Processing recipe data.')
    df_vinepair = create_recipe_dataframe(f"{args.recipe_directory}/vinepair/")
    logging.info('Recipe data ingest complete.')

    # Analyze Data
    visualize_data(df_cocktails)

    app = Flask('cocktails')

    @app.route('/drink')
    def fetch_drink():
        start_time = time.perf_counter()

        output_example = df_cocktails.sample(n=1)
        html_recipe = print_recipe_info(output_example)
        logging.debug('/drink HTML of %s:\n%s', str(output_example['recipe_uuid']), html_recipe)

        end_time = time.perf_counter()
        total = end_time - start_time
        logging.info('Rendered recipe data in %s seconds', str(total))

        return f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>" \
               f"{html_recipe}"

    @app.route('/glizzy')
    def fetch_glizzy():
        start_time = time.perf_counter()

        output_example = df_vinepair.sample(n=1)
        html_recipe = print_recipe_info(output_example)
        logging.debug('/glizzy HTML of %s:\n%s', str(output_example['recipe_uuid']), html_recipe)

        end_time = time.perf_counter()
        total = end_time - start_time
        logging.info('Rendered recipe data in %s seconds', str(total))

        return f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>" \
               f"{html_recipe}"

    logging.info('Hosting cocktail data')
    serve(app, host='0.0.0.0', port=80)


if __name__ == "__main__":
    main()
