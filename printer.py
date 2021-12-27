from util import extract_nested_values
import pandas as pd


def print_ingredients(ingredients: pd.Series) -> str:
    message = '<h3>Ingredients:</h3>\n<ul>'
    for ingredient in ingredients[0]:
        name = list(ingredient.keys())[0]
        amounts = ingredient.values()
        unpacked = [list(extract_nested_values(amount)) for amount in amounts][0]
        unpacked = ' '.join(str(element) for element in unpacked)
        message = message + f'<li>{name}: {unpacked}</li>\n'
    message += "</ul>"
    return message


def print_steps(steps: pd.Series) -> str:
    message = '<h3>Steps:</h3><ul>'
    message += '\n'.join(f"<li>{step['step']}</li>" for step in steps[0])
    message += '</ul>'
    return message


def print_yield(yields: pd.Series) -> str:
    message = 'Yields '
    drink_yield = ' '.join(map(str, yields))
    message = message + drink_yield + '.'
    return message


def print_notes(notes: pd.Series) -> str:
    if not notes:
        return ''

    notes_message = '<br><h3>Notes:</h3><ul>'
    notes_message += '\n'.join(f'<li>{note}</li>' for note in notes)
    notes_message += '</ul>'
    return notes_message


def print_recipe_info(recipe: pd.DataFrame) -> str:
    message = '' 
    message += f'\n<h1>{recipe.recipe_name.values[0]}</h1>'
    message += f'\n{print_ingredients(recipe.ingredients.values)}'
    message += f'\n{print_steps(recipe.steps.values)}'
    message += f'\n{print_yield(recipe.yields.values[0])}'
    message += f'\n{print_notes(recipe.notes.values[0])}'

    return message