#!/usr/bin/env python3
from nicegui import ui
from data_model import *
from recipe import recipe_card
import store
import footer

def render_page(plan: MealPlan, shopping: ShoppingList) -> None:
    @ui.page('/recipes')
    def meal_plan_page():
        recipes = store.get_all_recipes()
        ui.page_title('mealapp')
        with ui.card(align_items='stretch').classes('w-full h-160'):
            ui.label('Recipes').classes('text-semibold text-2xl font-serif')
            with ui.scroll_area().classes('h-120'):
                grid_style = 'repeat(auto-fill, minmax(220px, 1fr))'
                with ui.grid(columns=grid_style).classes('w-full'):
                    for id, recipe in recipes.items():
                        recipe_card(plan, shopping, id, recipe, False)
            with ui.link(target='/add_recipe'):
                ui.button(text='Add Recipe').props('flat fab-mini color=grey').classes('bg-green-100')
            def dump_to_json():
                json_str = store.convert_recipes_to_json()
                with open("recipes.json", "w", encoding="utf-8") as file:
                    file.write(json_str)
            ui.button('Dump to json', on_click=dump_to_json)
        footer.render_footer()

