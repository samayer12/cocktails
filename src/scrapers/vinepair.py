"""Scrape vinepair.com for cocktail recipes"""

import requests
import re
import uuid
from bs4 import BeautifulSoup


url = "https://vinepair.com/cocktail-recipe/?fwp_paged=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
reqs = requests.get(url, headers=headers)
soup = BeautifulSoup(reqs.text, 'html.parser')

recipe_pattern = re.compile(".*cocktail-recipe/.+")


def scrape_recipe_page(url, link_store):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    reqs = requests.get(url, headers=headers)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    recipe_pattern = re.compile(".*cocktail-recipe/.+")
    for link in soup.find_all('a'):
        valid_link = link.get('href')
        if valid_link == None:
            continue
        if recipe_pattern.match(valid_link) and valid_link not in link_store:
            link_store.append(valid_link)
    return link_store


def parse_recipe_to_yaml(url):
    reqs = requests.get(url, headers=headers)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    postfix_pattern = re.compile(".* Recipe$")
    for title in soup.find_all('h1', {"class": "entry-title"}):
        name = title.text
        if postfix_pattern.match(name):
            name = name[:-7]

    with open("recipes/vinepair/" + name.lower().replace(" ", "_") + ".yaml", 'w') as out_yaml:
        recipe_uuid = uuid.uuid4()
        recipe_text = f"recipe_uuid: {str(recipe_uuid)}\n"
        recipe_text += f"recipe_name: {str(name)}\n"
        recipe_text += f"source_url: {url}\n"
        
        for recipe_yield in soup.find_all('p', {"class": "review-extra-meta"}):
            lines = recipe_yield.text.split("\n")
            yield_data = lines[1].split()
            if len(yield_data) == 1:
                yield_data.append("1")
            if len(yield_data) == 2:
                yield_data.append("units")
            recipe_text += f"yields:\n" \
                           f"  - amount: {yield_data[1]}\n" \
                           f"    unit: {yield_data[2]}\n"
        
        recipe_text += "ingredients:\n"
        for ingredients in soup.find_all('li', {"class": "recipeIngredient"}):
            for span in ingredients.find_all('span'):
                if span == None:
                    continue
                #print(span.text)
                ingredient_data = span.text.split("\t")
                if len(ingredient_data) != 3:
                    if len(ingredient_data) == 0:
                        continue
                    if len(ingredient_data) == 1:
                        ingredient_data = span.text.split()
                        if len(ingredient_data) == 1:
                            ingredient_data.insert(0, "unit")
                            ingredient_data.insert(0, "1")
                    try:
                        if ingredient_data[0] == "As needed":
                            ingredient_data.insert(0, "1")
                        elif ingredient_data[0] == "Garnish:":
                            ingredient_data[1] = " ".join(ingredient_data[1:])
                            ingredient_data[0] = "1"
                            ingredient_data.insert(1, "unit")
                            del ingredient_data[3:]
                        elif '/' in ingredient_data[1] or ingredient_data[1] in "½¼¾¾":
                            ingredient_data[0] = " ".join(ingredient_data[0:2])
                            del ingredient_data[1]
                        elif len(ingredient_data) == 2:
                            ingredient_data.insert(1, "unit")
                    except IndexError:
                        continue
                    if len(ingredient_data) > 3:
                        ingredient_data[2] = " ".join(ingredient_data[2:])
                recipe_text += f"  - {ingredient_data[2]}:\n" \
                               f"      amounts:\n" \
                               f"        - amount: {ingredient_data[0]}\n" \
                               f"          unit: {ingredient_data[1]}\n"
                
        recipe_text += "steps:\n"
        for steps in soup.find_all('ol', {"class": "recipeInstructionsList"}):
            for step in steps.find_all('li'):
                recipe_text +=f"  - step:" \
                              f"\n      {step.text}\n"
        out_yaml.write(recipe_text)
    

recipe_links = []
print("Scraping recipe links from website...")
for i in range(1, 35):
    url = "https://vinepair.com/cocktail-recipe/?fwp_paged=" + str(i)
    recipe_links = scrape_recipe_page(url, recipe_links)


for link in recipe_links:
    print("Parsing " + link + "...")
    parse_recipe_to_yaml(link)

len(recipe_links)