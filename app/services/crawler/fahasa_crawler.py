from typing import Any, Dict

from app.services.crawler_interface import CrawlerInterface
from app.helper import *
from bs4 import BeautifulSoup

API_URLS = {
    'fahasa': 'https://www.fahasa.com/fahasa_catalog/product/loadproducts?category_id=9&currentPage=1&limit=1&order=num_orders&series_type=0'
}

def fetchDataFromAPI(api_url):
    data = []
    total = fetchApi(api_url)['total_products']
    pages = total // 300 + 1
    print('Total pages: ', pages)
    for i in range(1, 3 + 1):
        print('Total requests: ', i)
        api_url = (f'https://www.fahasa.com/fahasa_catalog/product/loadproducts?category_id=9&currentPage={i}&limit=300'
                   f'&order=num_orders&series_type=0')
        data += fetchApi(api_url)['product_list']
    return data


def getBookDetail(url):
    data = {}
    custom_headers = {
        'User-Agent': 'hihi',
    }
    response = requests.get(url, headers=custom_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        attributes = soup.find('table', {'class': 'data-table'}).findAll('tr')
        for attribute in attributes:
            th_element = attribute.find('th')
            if th_element is not None:
                attribute_title = th_element.text.strip()
            else:
                continue
            attribute_value = attribute.find('td').text.strip()
            if attribute_title == "Tên Nhà Cung Cấp":
                data['publisher'] = attribute_value
            if attribute_title == "Tác giả":
                data['author'] = attribute_value
            if attribute_title == "Năm XB":
                data['publish_date'] = attribute_value
            if attribute_title == "Số trang":
                data['page_number'] = attribute_value
            if attribute_title == "Người Dịch":
                data['translator'] = attribute_value
            if attribute_title == "Kích thước":
                data['size'] = attribute_value
        print(data)
        return data
    else:
        print('Error!')
        print(response.status_code)
    return


def scrapeBookList(url):
    data = fetchDataFromAPI(url)
    filename = 'fahasa.csv'
    fieldnames = ['product_id', 'product_name', 'image_src', 'product_url', 'discount', 'product_price', 'product_url']
    writeCSV(filename, data, fieldnames)


class FahasaCrawler(CrawlerInterface):

    def crawl(self) -> Dict[str, Any]:
        # Implement the logic specific to the Fahasa crawler
        data = fetchDataFromAPI(API_URLS['fahasa'])

        filename = 'fahasa.csv'

        fieldnames = ['product_id', 'product_name', 'image_src', 'product_url', 'discount', 'product_price',
                      'product_url']

        writeCSV(filename, data, fieldnames)

        data = readCSV(filename, fieldnames)
        return data
