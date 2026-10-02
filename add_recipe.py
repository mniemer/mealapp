#!/usr/bin/env python3
from nicegui import ui
from data_model import *
import store
import requests
from lxml import html
import footer

def add_nyt(url: str) -> None:
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        name = [el.text for el in tree.find_class('pantry--title-display')][0]
        img_srcset = tree.xpath(".//img[contains(@class, 'headermediacarousel_image__Jq9NO')]/@srcset")[0]
        img_src_all = img_srcset.split(',')[0]
        base, ext, _ = img_src_all.rpartition(".jpg")
        img_url = base + ext
        ingredients = [Ingredient(el.text, "") for el in tree.find_class('ingredient_ingredient__rfjvs')]
        step_elements = tree.find_class('preparation_step__nzZHP')
        steps = []
        for li in step_elements:
            p_tags = li.xpath(".//p")
            for p in p_tags:
                steps.append(p.text_content().strip())
        new_recipe = Recipe(name, img_url, steps, ingredients)
        new_id = store.add_recipe(new_recipe)
        ui.navigate.to('/recipe/' + new_id)
    except Exception as e:
        ui.label('Failed importing recipe: ' + str(e))

def render_page() -> None:
    @ui.page('/add_recipe')
    def meal_plan_page():
        with ui.card(align_items='stretch').classes('w-150'):
            ui.label('Add Recipe').classes('text-semibold text-2xl font-serif')
            with ui.tabs().classes('w-full') as tabs:
                form = ui.tab('Form')
                link = ui.tab('Link')
            with ui.tab_panels(tabs, value=form).classes('w-full'):
                with ui.tab_panel(form):
                    name = ui.input(label='Recipe name').props('dense').classes('w-full')
                    image_url = ui.input(label='Image URL (optional)').props('dense').classes('w-full')
                    ingredients_input = ui.textarea(label='Ingredients', 
                                              placeholder='Separate each ingredient with a new line and ingredients from their amounts with a pipe. Amounts are optional. Ex:\njalapeño pepper | 1\nonion | 1/2 medium\ncumin').classes('w-full')
                    steps_input = ui.textarea(label='Steps', placeholder='Separate each step with a new line.')
                    def submit(name: str, image_url: str, ingredients_raw: str, steps_raw: str):
                        ingredients_split = [item.split("|") for item in ingredients_raw.splitlines()]
                        def make_ingredient(i: list[str]) -> Ingredient:
                            n = i[0].strip()
                            if len(i) > 1:
                                a = i[1].strip()
                            else :
                                a = ''
                            return Ingredient(n, a)
                        ingredients = list(map(lambda i: make_ingredient(i), ingredients_split))
                        steps = steps_raw.splitlines()
                        new_recipe = Recipe(name.strip(), image_url.strip(), steps, ingredients)
                        new_id = store.add_recipe(new_recipe)
                        ui.navigate.to('/recipe/' + new_id)
                    ui.button(text='Submit', on_click=lambda: submit(name.value, image_url.value, ingredients_input.value, steps_input.value))
                with ui.tab_panel(link):
                    nyt_url = ui.input('Recipe URL (NYT Cooking only)').props('dense').classes('w-full')
                    ui.button('Submit', on_click=lambda: add_nyt(nyt_url.value))
        footer.render_footer()