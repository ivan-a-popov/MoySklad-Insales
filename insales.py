from requests.auth import HTTPBasicAuth
import setup
import requests

from setup import INSALES_BASE_URL, INSALES_API_ID, INSALES_API_PASS, INSALES_PER_PAGE


def put_image(code, url):
    endpoint = f'products/{code}/images.json'
    api_endpoint = f'{INSALES_BASE_URL}/{endpoint}'
    setup.logger.debug(f"Updating {api_endpoint}")
    data = {
        "image": {
            "src": url
        }
    }
    response = requests.post(api_endpoint, auth=HTTPBasicAuth(INSALES_API_ID, INSALES_API_PASS), json=data)
    if not response.ok:
        setup.logger.error(response)
    else:
        setup.logger.debug("Done")


def get_qty():
    url = INSALES_BASE_URL + '/products/count.json'
    response = requests.get(url, auth=HTTPBasicAuth(INSALES_API_ID, INSALES_API_PASS))
    if not response.ok:
        setup.logger.error(f'Error connecting InSales. Server returned: {response}')
        exit(1)
    else:
        qty = response.json()['count']
        return qty


def get_page(page):
    endpoint = f'products.json?per_page={INSALES_PER_PAGE}&page={page}'
    api_endpoint = f'{INSALES_BASE_URL}/{endpoint}'
    setup.logger.debug(f"Getting page {page}: {api_endpoint}")
    response = requests.get(api_endpoint, auth=HTTPBasicAuth(INSALES_API_ID, INSALES_API_PASS))
    if not response.ok:
        setup.logger.error(response)
    else:
        setup.logger.debug("OK")
        if setup.DEBUG:
            setup.save_debug_file(f'insales_page_{page}.txt', response.json())
    return response.json()


def get_goods():
    setup.logger.debug("Getting data from InSales")
    qty = get_qty()
    count = qty // INSALES_PER_PAGE + 1
    setup.logger.debug(f"{qty} items, {count} pages")
    goods = []
    for i in range(1, count+1):
        page = get_page(i)
        goods += page
    if setup.DEBUG:
        setup.save_debug_file('insales_all.txt', goods)
    goods_without_img = []
    for good in goods:
        if not good['images']:
            goods_without_img.append(good)
    if setup.DEBUG:
        setup.save_debug_file('insales_no_img.txt', goods_without_img)
    result = {}
    for good in goods_without_img:
        result[good['product_field_values'][0]['value']] = good['id']
    return result

if __name__ == '__main__':
    get_goods()
