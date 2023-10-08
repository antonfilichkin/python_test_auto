import os
import sys
import timeit

import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

sp_url = 'https://markets.businessinsider.com'

max_workers = min(32, os.cpu_count() + 4)
if len(sys.argv) > 1:
    max_workers = int(sys.argv[1])

class Company:
    def __init__(self, name: str, url: str, year_change: str):
        self.name = name
        self.code = None
        self.url = f'{sp_url}{url}'
        self.price = None
        self.year_change = float(year_change.replace('%', ''))
        self.pe_ratio = None

    def __json__(self):
        return {
            'code': self.code,
            'name': self.name,
            'price': self.price,
            'pe_ratio': self.pe_ratio,
            'growth': self.year_change
        }


def _fetch_html(url: str) -> str:
    return requests.get(url).text


def _collect_companies_from_table(url: str) -> list[Company]:
    companies = []

    html = _fetch_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('main').find('tbody')
        if table:
            for row in table.findAll('tr'):
                name = row.find('a').get_text()
                url = row.find('a').get('href')
                year_change = row.find_all('td')[-1].find_all('span')[-1].get_text()
                companies.append(Company(name, url, year_change))

    return companies


def _enrich_company_info_from_page(company: Company) -> Company:
    html = _fetch_html(company.url)
    soup = BeautifulSoup(html, 'html.parser')
    company.price = float(soup.find('span', class_='price-section__current-value').get_text().replace(',', ''))
    company.code = soup.find('span', class_='price-section__category').find('span').get_text().replace(', ', '')
    pe_label = soup.find('div', class_='snapshot__header', string='P/E Ratio')
    if pe_label:
        pe_value = pe_label.find_parent('div', class_='snapshot__data-item').find(string=True, recursive=False).strip()
        company.pe_ratio = float(pe_value)

    return company


def main():
    table_page_url = f'{sp_url}/index/components/s&p_500?p='

    companies = []

    table_page_urls = [f'{table_page_url}{page}' for page in range(1, 12)]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        companies.extend(pool.map(_collect_companies_from_table, table_page_urls))

    companies = [company for table_page_companies in companies for company in table_page_companies]

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        pool.map(_enrich_company_info_from_page, companies)

    def sort_key(company: Company, field: str):
        if field == 'pe_ratio':
            if company.pe_ratio is None:
                return float('inf')
            else:
                return company.pe_ratio

    results = {
        'most_expensive': sorted(companies, key=lambda company: company.price, reverse=True)[:10],
        'lowest_pe': sorted(companies, key=lambda company: sort_key(company, 'pe_ratio'))[:10],
        'most_grow': sorted(companies, key=lambda company: company.year_change, reverse=True)[:10]
    }

    for name, result in results.items():
        with open(f'{name}.json', 'w') as file:
            json_result = json.dumps(result, default=lambda company: company.__json__(), indent=4)
            file.write(json_result)

    print(f"Multithread - parsed '{len(companies)}' companies (max workers - {max_workers})")


if __name__ == '__main__':
    execution_time = timeit.timeit(main, number=1)
    print(f'Execution time: {execution_time} seconds')
