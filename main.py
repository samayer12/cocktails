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
    message = ''
    # TODO less dict unpacking jank
    # TODO look into tabulate library
    for ingredient in ingredients[0]:
        name = list(ingredient.keys())[0]
        amounts = ingredient.values()
        unpacked = [list(extract_nested_values(amount)) for amount in amounts][0]
        unpacked = ' '.join(str(element) for element in unpacked)
        message = message + f'{name}: {unpacked}\n'

    return message


def print_steps(steps: pd.Series) -> str:
    return '\n'.join(step['step'] for step in steps[0])


def main():
    path_to_yml = 'recipes/apple_martini.yml'
    with open(path_to_yml) as yml_file:
        yml_contents = load(yml_file, Loader=SafeLoader)
    df_cocktails = pd.json_normalize(yml_contents)
    print(df_cocktails)
    print(print_ingredients(df_cocktails.ingredients))
    print(print_steps(df_cocktails.steps))


if __name__ == "__main__":
    main()
