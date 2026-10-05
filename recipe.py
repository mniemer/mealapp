#!/usr/bin/env python3
from nicegui import ui
from data_model import *
import store
import footer

def add_to_meal_plan(plan: MealPlan, shopping: ShoppingList, id: str) -> None:
    recipe = store.get_recipe(id)
    plan.add_recipe(id, recipe)
    for ingredient in recipe.ingredients:
        shopping.add(ingredient.name, ingredient.amount)
    ui.notify('Added to meal plan')
    return

def remove_from_meal_plan(plan: MealPlan, id: str) -> None:
    plan.remove_recipe(id)
    ui.notify('Removed from meal plan')
    return

def render_page() -> None:
    @ui.page('/recipe/{id}')
    def recipe_page(id: str):
        recipe = store.get_recipe(id)
        ui.page_title('mealapp')
        with ui.card(align_items='stretch').classes('w-full h-160'):
            with ui.grid(columns='1fr 2fr'):
                ui.image(recipe.img_url)
                ui.label(recipe.name).classes('text-semibold text-2xl font-serif')
            with ui.tabs().classes('w-full').props('align=left') as tabs:
                ingredients = ui.tab('Ingredients')
                steps = ui.tab('Steps')
            with ui.tab_panels(tabs, value=ingredients).classes('w-full'):
                with ui.tab_panel(ingredients):
                    with ui.list().props('dense separator border').classes('w-full'):
                        for ingredient in recipe.ingredients:
                            with ui.item():
                                with ui.grid(columns='1fr auto').classes('w-full'):
                                    ui.label(ingredient.name)
                                    ui.label(ingredient.amount)
                with ui.tab_panel(steps):
                    with ui.list().props('dense separator border').classes('w-full'):
                        for step in recipe.steps:
                            with ui.item():
                                ui.label(step)
        footer.render_footer()

def recipe_card(plan: MealPlan, shopping: ShoppingList, id: str, recipe: Recipe, remove: bool = False):
    with ui.card().classes('w-60').tight():
        with ui.card_section().props('horizontal'):
            ui.label(recipe.name)
            target_path = '/recipe/' + id
            with ui.link(target=target_path):
                ui.image(recipe.img_url).classes('w-30 h-30')
        if remove:
            ui.button(icon='delete', on_click=lambda: remove_from_meal_plan(plan, id)).classes('absolute top-1 right-1 bg-white').props('flat fab-mini color=grey')
        else:
            ui.button(icon='add', on_click=lambda: add_to_meal_plan(plan, shopping, id)).classes('absolute top-1 right-1 bg-white').props('flat fab-mini color=grey')


