from pytest_check import check_func

from helpers import dataclass_from_dict


@check_func
def has_ingredient(beer, root_path, expected_ingredient, message='Ingredient check'):
    ingredients = beer['ingredients']
    try:
        actual_ingredient = next(h for h in ingredients[root_path] if h['name'] == expected_ingredient.name)
    except StopIteration:
        assert False, (f"Was not able to find '{expected_ingredient.name}' ingredient!"
                       f" Actual ingredient list: '{[h['name'] for h in ingredients[root_path]]}'")
    assert dataclass_from_dict(type(expected_ingredient), actual_ingredient) == expected_ingredient, message
