"""
Please, complete the following task.


You will work with this endpoint - https://api.punkapi.com/v2/beers/8
 Need to write 2 tests:


 1. Using requests method GET need to check that:
 * status code - 200
 * name - Fake Lager
 * abv - 4.7


 2. Using requests method DELETE need to check that:
 * status code - 404
 * message - No endpoint found that matches '/v2/beers/8'
"""
from pytest_check import check
import requests

base_path = 'https://api.punkapi.com'
endpoint_ut = '/v2/beers/8'


def test_1_get():
    response = requests.get(base_path + endpoint_ut)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    beer = body[0]
    check.equal(beer['name'], 'Fake Lager', 'Name check')
    check.equal(beer['abv'], 4.7, 'ABV check')
    check.equal(beer['method']['fermentation']['temp']['value'], 10, 'Fermentation temp check')
    acidulated_malt = next(malt for malt in beer['ingredients']['malt'] if malt['name'] == 'Acidulated Malt')
    check.equal(acidulated_malt['amount']['value'], 0.07, 'Acidulated Malt amount check')


def test_2_delete():
    response = requests.delete(base_path + endpoint_ut)
    assert response.status_code == 404
    assert response.json()['message'] == f"No endpoint found that matches '{endpoint_ut}'"
