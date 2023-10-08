import timeit
import requests

from __shared__ import *


def _fetch_html_(url: str) -> str:
    return requests.get(url).text


def _collect_companies_(url: str) -> list[Company]:
    html = _fetch_html_(url)
    return collect_companies_from_table(html)


def _enrich_(company: Company) -> Company:
    html = _fetch_html_(company.url)
    return enrich_company_info_from_page(company, html)


def _main_(pages: int) -> int:
    companies = []

    for page in range(1, pages + 1):
        companies.extend(_collect_companies_(f'{table_page_url}{page}'))

    for company in companies:
        _enrich_(company)

    write_results(companies)
    return len(companies)


def execute(pages: int = 1) -> int:
    return _main_(pages)


if __name__ == '__main__':
    execution_time = timeit.timeit(lambda: execute(pages_to_parse()), number=1)
    print(f"Sync - execution time: {execution_time:.2f} seconds.")
