import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup

sp_url = 'https://markets.businessinsider.com'


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
            "code": self.code,
            "name": self.name,
            "price": self.price,
            "pe_ratio": self.pe_ratio,
            "growth": self.year_change
        }


async def _fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return ''


def _collect_companies_from_table(html: str) -> list[Company]:
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('main').find('tbody')
        companies = []
        for row in table.findAll('tr'):
            name = row.find('a').get_text()
            url = row.find('a').get('href')
            year_change = row.find_all('td')[-1].find_all('span')[-1].get_text()
            companies.append(Company(name, url, year_change))
        return companies
    return []


def _enrich_company_info_from_page(company: Company, html: str) -> Company:
    soup = BeautifulSoup(html, 'html.parser')
    company.price = float(soup.find('span', class_='price-section__current-value').get_text())

    company.code = soup.find('span', class_='price-section__category').find('span').get_text().replace(', ', '')

    pe_label = soup.find('div', class_='snapshot__header', string='P/E Ratio')
    if pe_label:
        pe_value = pe_label.find_parent('div', class_='snapshot__data-item').find(string=True, recursive=False).strip()
        company.pe_ratio = float(pe_value)

    return company


async def main():

    fetch_table_page_tasks = [_fetch_html(f'{sp_url}/index/components/s&p_500?p={page}') for page in range(1, 2)]
    table_pages = await asyncio.gather(*fetch_table_page_tasks)

    companies = []
    for page in table_pages:
        companies.extend(_collect_companies_from_table(page))

    fetch_company_data_tasks = [_fetch_html(company.url) for company in companies]
    companies_pages = await asyncio.gather(*fetch_company_data_tasks)

    for company, company_page in zip(companies, companies_pages):
        _enrich_company_info_from_page(company, company_page)

    def sort_key(company: Company, field: str):
        if field == 'pe_ratio':
            if company.pe_ratio is None:
                return float('inf')
            else:
                return company.pe_ratio

    results = {
        "most_expensive": sorted(companies, key=lambda company: company.price, reverse=True)[:10],
        "lowest_pe": sorted(companies, key=lambda company: sort_key(company, 'pe_ratio'))[:10],
        "most_grow": sorted(companies, key=lambda company: company.year_change, reverse=True)[:10]
    }

    for name, result in results.items():
        with open(f'{name}.json', 'w') as file:
            json_result = json.dumps(result, default=lambda company: company.__json__(), indent=4)
            file.write(json_result)


if __name__ == '__main__':
    asyncio.run(main())
