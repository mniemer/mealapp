#!/usr/bin/env python3
from collections.abc import Callable
from dataclasses import dataclass, field

@dataclass
class Ingredient:
    name: str
    amount: str

@dataclass
class Recipe:
    name: str
    img_url: str
    steps: list[str] = field(default_factory=list)
    ingredients: list[Ingredient] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.ingredients, list):
            self.ingredients = [
                Ingredient(**i) if isinstance(i, dict) else i
                for i in self.ingredients
            ]

@dataclass
class MealPlan:
    on_change: Callable
    recipes: dict[str, Recipe] = field(default_factory=dict)

    def add_recipe(self, id: str, recipe: Recipe) -> None:
        self.recipes[id] = recipe
        self.on_change()

    def remove_recipe(self, id) -> None:
        del self.recipes[id]
        self.on_change()

@dataclass
class ShoppingItem:
    name: str
    amount: str
    done: bool = False

@dataclass
class ShoppingList:
    on_change: Callable
    items: list[ShoppingItem] = field(default_factory=list)

    def add(self, name: str, amount: str, done: bool = False) -> None:
        self.items.append(ShoppingItem(name, amount, done))
        self.items.sort(key=lambda item: item.name)
        self.on_change()

    def remove(self, item: ShoppingItem) -> None:
        self.items.remove(item)
        self.on_change()
