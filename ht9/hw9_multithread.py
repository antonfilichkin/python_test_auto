import timeit
import os
import sys
import requests
from concurrent.futures import ThreadPoolExecutor

from __shared__ import *

max_workers = min(32, os.cpu_count() + 4)
if len(sys.argv) > 1:
    max_workers = int(sys.argv[1])


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

    table_page_urls = [f'{table_page_url}{page}' for page in range(1, 12)]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        companies.extend(pool.map(_collect_companies_, table_page_urls))

    companies = [company for table_page_companies in companies for company in table_page_companies]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        pool.map(_enrich_, companies)

    write_results(companies)
    print(f"Multithread - parsed '{len(companies)}' companies.")


if __name__ == '__main__':
    execution_time = timeit.timeit(main, number=1)
    print(f'Multithread - execution time: {execution_time:.2f} seconds.')
