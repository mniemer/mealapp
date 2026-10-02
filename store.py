#!/usr/bin/env python3
import json
from dataclasses import asdict
from data_model import *

def load_recipes_from_json() -> dict[str, Recipe]:
    with open('recipes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        unpacked_recipes: dict[str, Recipe] = {
            key: Recipe(**value) for key, value in data.items()
        }
        return unpacked_recipes
    
def get_next_id() -> str:
    global curr_id
    curr_id += 1
    return 'r' + str(curr_id)

def get_all_recipes() -> dict[str, Recipe]:
    return recipes

def get_recipe(id: str) -> Recipe:
    return recipes[id]

def convert_recipes_to_json() -> str:
    return json.dumps(recipes, default=asdict)

def add_recipe(recipe: Recipe) -> str:
    id = get_next_id()
    recipes[id] = recipe
    return id

recipes = load_recipes_from_json()
ids = list(map(lambda id: int(id[1:]), recipes.keys()))
curr_id = max(ids)
