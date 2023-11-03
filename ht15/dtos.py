from dataclasses import dataclass


@dataclass
class Ingredient:
    name: str
    amount: type('Amount', (object,), {'value': float, 'unit': str})


@dataclass
class IngredientWithInstructions(Ingredient):
    add: str
    attribute: str
