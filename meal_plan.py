#!/usr/bin/env python3
from nicegui import ui
from data_model import *
import recipe
import footer

@ui.refreshable
def meal_plan_ui(plan: MealPlan, shopping: ShoppingList):
    with ui.card(align_items='stretch').classes('w-150 h-160'):
        ui.label('Meal plan').classes('text-semibold text-2xl font-serif')
        if not plan.recipes:
            ui.label('No recipes')
            return
        with ui.scroll_area().classes('h-120'):
            with ui.grid(columns=2):
                for id, item in plan.recipes.items():
                    recipe.recipe_card(plan, shopping, id, item, True)

def render_page(plan: MealPlan, shopping: ShoppingList) -> None:
    @ui.page('/')
    def meal_plan_page():
        meal_plan_ui(plan, shopping)
        footer.render_footer()