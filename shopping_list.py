#!/usr/bin/env python3
from nicegui import ui

from data_model import *
import footer

# TODO shopping list
# - Clear all button
# - Categorization of common list items
# - Option to make "done" items not visible
# - (only do from recipes) Items with same name aggregate on add

@ui.refreshable
def shopping_ui(shopping_list: ShoppingList):
    if not shopping_list.items:
        ui.label('List is empty')
        return
    ui.linear_progress(sum(item.done for item in shopping_list.items) / len(shopping_list.items), show_value=False, color='green')
    with ui.scroll_area().classes('h-120'):
        with ui.list().props('dense separator border').classes('w-full'):
            for item in shopping_list.items:
                with ui.item():
                    with ui.grid(columns='auto 1fr auto auto').classes('w-full gap-0 items-center'):
                        ui.checkbox(value=item.done, on_change=shopping_ui.refresh).bind_value(item, 'done').props('dense')
                        ui.label(item.name)
                        ui.label(item.amount)
                        ui.button(on_click=lambda item=item: shopping_list.remove(item), 
                                icon='delete').props('flat fab-mini color=grey')


def render_page(shopping_list: ShoppingList) -> None:
    @ui.page('/shopping_list')
    def shopping_list_page():
        with ui.card(align_items='stretch').classes('w-150 h-160'):
            ui.label('Shopping list').classes('text-semibold text-2xl font-serif')
            shopping_ui(shopping_list)
            with ui.row(align_items='center'):
                new_item_name = ui.input('New item').props('dense')
                new_item_amount = ui.input('Amount').props('dense')
                def submit():
                     shopping_list.add(new_item_name.value, new_item_amount.value)
                     new_item_name.set_value(None)
                     new_item_amount.set_value(None)
                ui.button(text='Add', on_click=submit).props('flat fab-mini color=grey') \
                    .classes('bg-green-100').bind_enabled_from(new_item_name, 'value') 
        
        footer.render_footer()