from dataclasses import dataclass


@dataclass
class Amount:
    value: float
    unit: str


@dataclass
class Ingredient:
    name: str
    amount: Amount


@dataclass
class IngredientWithInstructions(Ingredient):
    add: str
    attribute: str
