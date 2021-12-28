import logging
import pandas as pd

from util import extract_nested_values

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

def print_refresh_button() -> str:
    message = '<div><button type="button" onclick="window.location.reload();">New Cocktail</button></div>'
    return message

def print_recipe_info(recipe: pd.DataFrame) -> str:
    if pd.Series(['recipe_name', 'ingredients', 'steps', 'yields', 'notes']).isin(recipe.columns).all():
        message = '' 
        message += f'\n<h1>{recipe.recipe_name.values[0]}</h1>'
        message += f'\n{print_ingredients(recipe.ingredients.values)}'
        message += f'\n{print_steps(recipe.steps.values)}'
        message += f'\n{print_yield(recipe.yields.values[0])}'
        message += f'\n{print_notes(recipe.notes.values[0])}'
        message += f'\n{print_refresh_button()}'
    
        return message
    else:
        logging.error('Missing column for %s', str(recipe.recipe_uuid))
        error_message = f"<b>Oops!</b> The data for this cocktail is corrupted." \
                        f"Don\'t worry, we\'ve logged the issue and know about it now." \
                        f"If you really want to pester someone, let Braden know."
        error_message += f"<br>UUID: {recipe.recipe_uuid.values[0]}<br>Recipe Name: {recipe.recipe_name.values[0]}"
        return error_message