#!/usr/bin/env python3
from collections.abc import Callable

from nicegui import ui

import gallery
import shopping_list
import recipe
import meal_plan
import add_recipe
from data_model import *


# TODO structural
# - Host & deploy (docker image-> heroku)
# - how are clients getting updated when one user makes a change? -> might just work
# - store recipes, meal plan, shopping list in DB
# - writes to DB when updating meal plan & shopping list


shopping = ShoppingList(on_change=shopping_list.shopping_ui.refresh)
plan = MealPlan(on_change=meal_plan.meal_plan_ui.refresh)

ui.button.default_classes('font-sans')
ui.label.default_classes('font-sans')
ui.input.default_classes('font-sans')
ui.textarea.default_classes('font-sans w-full')

meal_plan.render_page(plan, shopping)
gallery.render_page(plan, shopping)
recipe.render_page()
shopping_list.render_page(shopping)
add_recipe.render_page()

ui.run(favicon='🥑', port=8080)