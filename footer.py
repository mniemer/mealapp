#!/usr/bin/env python3
from collections.abc import Callable
from dataclasses import dataclass, field
from nicegui import ui

# TODO footer
# - make it look better - tabs for selected page and icons              
            
def render_footer() -> None:
    with ui.row():
        ui.link('Meal plan', '/')
        ui.link('Recipes', '/recipes')
        ui.link('Shopping List', '/shopping_list')