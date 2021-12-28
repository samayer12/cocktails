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


recipe_links = []
for link in soup.find_all('a'):
    valid_link = link.get('href')
    if valid_link == None:
        continue
    if recipe_pattern.match(valid_link) and valid_link not in recipe_links:
        recipe_links.append(valid_link)


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


url = "https://vinepair.com/cocktail-recipe/paloma/"
reqs = requests.get(url, headers=headers)
soup = BeautifulSoup(reqs.text, 'html.parser')

out_yaml = open('paloma.yaml', 'a')

recipe_uuid = uuid.uuid4()
print(str(recipe_uuid))
out_yaml.write("recipe_uuid: " + str(recipe_uuid) + "\n")

postfix_pattern = re.compile(".* Recipe$")
for title in soup.find_all('h1', {"class": "entry-title"}):
    name = title.text
    if postfix_pattern.match(name):
        name = name[:-7]
    print(name)
    out_yaml.write("recipe_name: " + name + "\n")

out_yaml.write("source_url: " + url + "\n")

for recipe_yield in soup.find_all('p', {"class": "review-extra-meta"}):
    print(recipe_yield.text)
    yield_data = recipe_yield.text.split()
    out_yaml.write("yields:\n  - amount: "+ yield_data[1] + "\n" + "    unit: " + yield_data[2] + "\n")


out_yaml.write("ingredients:\n")
for ingredients in soup.find_all('li', {"class": "recipeIngredient"}):
    for span in ingredients.find_all('span'):
        print(span.text)
        if span == None:
            continue
        ingredient_data = span.text.split("\t")
        if len(ingredient_data) == 2:
            if ingredient_data[0] == "As needed":
                ingredient_data.insert(0, "1")
        out_yaml.write("  - " + ingredient_data[2] + 
                       ":\n      amounts:\n        - amount: " + 
                       ingredient_data[0] + 
                       "\n          unit: "  + 
                       ingredient_data[1] + "\n")


out_yaml.write("steps:\n")
for steps in soup.find_all('ol', {"class": "recipeInstructionsList"}):
    for step in steps.find_all('li'):
        print(step.text)
        out_yaml.write("  - step:\n      " + step.text + "\n")


out_yaml.close()


def parse_recipe_to_yaml(url):
    reqs = requests.get(url, headers=headers)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    postfix_pattern = re.compile(".* Recipe$")
    for title in soup.find_all('h1', {"class": "entry-title"}):
        name = title.text
        if postfix_pattern.match(name):
            name = name[:-7]
    out_yaml = open("scrapers/vinepair/" + name.lower().replace(" ", "_") + ".yaml", 'a')
    
    recipe_uuid = uuid.uuid4()
    out_yaml.write("recipe_uuid: " + str(recipe_uuid) + "\n")
    
    out_yaml.write("recipe_name: " + name + "\n")
    
    out_yaml.write("source_url: " + url + "\n")
    
    for recipe_yield in soup.find_all('p', {"class": "review-extra-meta"}):
        lines = recipe_yield.text.split("\n")
        yield_data = lines[1].split()
        if len(yield_data) == 1:
            yield_data.append("1")
        if len(yield_data) == 2:
            yield_data.append("units")
        out_yaml.write("yields:\n  - amount: "+ yield_data[1] + "\n" + "    unit: " + yield_data[2] + "\n")
    
    out_yaml.write("ingredients:\n")
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
            out_yaml.write("  - " + ingredient_data[2] + 
                           ":\n      amounts:\n        - amount: " + 
                           ingredient_data[0] + 
                           "\n          unit: "  + 
                           ingredient_data[1] + "\n")
            
    out_yaml.write("steps:\n")
    for steps in soup.find_all('ol', {"class": "recipeInstructionsList"}):
        for step in steps.find_all('li'):
            out_yaml.write("  - step:\n      " + step.text + "\n")
    
    out_yaml.close()


recipe_links = []
print("Scraping recipe links from website...")
for i in range(1, 35):
    url = "https://vinepair.com/cocktail-recipe/?fwp_paged=" + str(i)
    recipe_links = scrape_recipe_page(url, recipe_links)


for link in recipe_links:
    print("Parsing " + link + "...")
    parse_recipe_to_yaml(link)

len(recipe_links)