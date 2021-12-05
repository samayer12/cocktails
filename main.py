import argparse
import glob
import logging
import time

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
    message = 'Ingredients:\n'
    # TODO less dict unpacking jank
    # TODO look into tabulate library
    for ingredient in ingredients[0]:
        name = list(ingredient.keys())[0]
        amounts = ingredient.values()
        unpacked = [list(extract_nested_values(amount)) for amount in amounts][0]
        unpacked = ' '.join(str(element) for element in unpacked)
        message = message + f'- {name}: {unpacked}\n'

    return message


def print_steps(steps: pd.Series) -> str:
    return '\n'.join(step['step'] for step in steps[0])


def print_yield(yields: pd.Series) -> str:
    message = 'Yields '

    for result in yields:
        unpacked = [list(extract_nested_values(result)) for result in yields][0]
        unpacked = ' '.join(str(element) for element in unpacked)
        message = message + unpacked + '.'
    return message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('recipe_directory', type=str)
    parser.add_argument('log_file', type=str)
    args = parser.parse_args()

    logging.basicConfig(filename=f'log/{args.log_file}', level=logging.INFO, force=True,
                        format='%(asctime)s, %(levelname)s, %(name)s, %(message)s')
    logging.info('Start')
    logging.info('Processing recipe data')

    start_time = time.perf_counter()

    recipe_files = glob.glob(f'{args.recipe_directory}/*.yml')
    df_cocktails = pd.DataFrame()

    for file in recipe_files:
        with open(file) as yml_file:
            yml_contents = load(yml_file, Loader=SafeLoader)
        df_cocktails = pd.json_normalize(yml_contents)

    print(df_cocktails)
    print(df_cocktails.recipe_name.values)
    print(print_ingredients(df_cocktails.ingredients))
    print(print_steps(df_cocktails.steps))
    print(print_yield(df_cocktails.yields))

    end_time = time.perf_counter()
    total = end_time - start_time

    logging.info('Processing recipe data complete in %s seconds', str(total))
    logging.info('End')


if __name__ == "__main__":
    main()
