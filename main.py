import pandas as pd
from yaml import SafeLoader, load


def main():
    path_to_yml = 'recipes/apple_martini.yml'
    with open(path_to_yml) as yml_file:
        yml_contents = load(yml_file, Loader=SafeLoader)
    df_cocktails = pd.json_normalize(yml_contents)
    print(df_cocktails)


if __name__ == "__main__":
    main()
