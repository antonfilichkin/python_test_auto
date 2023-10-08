import timeit
import aiohttp
import asyncio

from __shared__ import *


async def _fetch_html_(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def _collect_companies_(url: str) -> list[Company]:
    html = await _fetch_html_(url)
    return collect_companies_from_table(html)


async def _enrich_(company: Company) -> Company:
    html = await _fetch_html_(company.url)
    return enrich_company_info_from_page(company, html)


async def main():
    fetch_companies_tasks = [_collect_companies_(f'{table_page_url}{page}') for page in range(1, 12)]
    companies = await asyncio.gather(*fetch_companies_tasks)

    companies = [company for table_page_companies in companies for company in table_page_companies]

    fetch_company_data_tasks = [_enrich_(company) for company in companies]
    companies = await asyncio.gather(*fetch_company_data_tasks)

    write_results(companies)
    print(f"Async - parsed '{len(companies)}' companies")


def run_async_main():
    asyncio.run(main())


if __name__ == '__main__':
    execution_time = timeit.timeit(run_async_main, number=1)
    print(f'Async - execution time: {execution_time:.2f} seconds')