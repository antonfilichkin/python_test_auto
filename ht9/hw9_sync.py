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


def main():
    companies = []

    for page in range(1, 12):
        companies.extend(_collect_companies_(f'{table_page_url}{page}'))

    for company in companies:
        _enrich_(company)

    write_results(companies)
    print(f"Sync - parsed '{len(companies)}' companies.")


if __name__ == '__main__':
    execution_time = timeit.timeit(main, number=1)
    print(f"Sync - execution time: {execution_time:.2f} seconds.")
