import base64
import requests
import setup

from setup import MOYSKLAD_NAME, MOYSKLAD_SECRET, MOYSKLAD_BASE_URL, MOYSKLAD_TOKEN, MOYSKLAD_PER_PAGE


def get_auth():
    """Вспомогательная функция для получения токена авторизации
    по логину и паролю. Используется только один раз.
    """
    endpoint = 'security/token'
    auth_header = base64.b64encode(bytes(f'{MOYSKLAD_NAME}:{MOYSKLAD_SECRET}'.encode('ascii'))).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}'}
    api_endpoint = f'{MOYSKLAD_BASE_URL}/{endpoint}'
    response = requests.request("POST", api_endpoint, headers=headers)
    return response.text.encode('utf8')


def get_page(url):
    setup.logger.debug(f"Getting data from moysklad: {url}")
    headers = {'Authorization': f'Bearer {MOYSKLAD_TOKEN}'}
    response = requests.request("GET", url, headers=headers)
    if not response.ok:
        setup.logger.error(response)
    return response.json()


def get_goods():
    """Функция возвращает массив товаров, у которых есть фотографии
    как словарь вида {внешний код: код МойСклад}
    """
    endpoint = f'entity/assortment?limit={MOYSKLAD_PER_PAGE}'
    next_href = f'{MOYSKLAD_BASE_URL}/{endpoint}'
    goods_with_img = []

    while next_href:
        page = get_page(next_href)
        for good in page['rows']:
            if good['meta']['type'] == 'product':
                if good['images']['meta']['size']:
                    goods_with_img.append(good)
        try:
            next_href = page['meta']['nextHref']
        except KeyError:
            break

    if setup.DEBUG:
        setup.save_debug_file('ms_with_img.txt', goods_with_img)

    result = {}
    for good in goods_with_img:
        result[good['externalCode']] = good['id']
    return result


def get_images(code):
    """Функция возвращает список фотографий по коду товара"""
    headers = {
        'Authorization': f'Bearer {MOYSKLAD_TOKEN}'
    }
    api_endpoint = f'{MOYSKLAD_BASE_URL}/entity/product/{code}/images'
    setup.logger.debug(f"Getting pictures from moysklad: {api_endpoint}")
    response = requests.request("GET", api_endpoint, headers=headers)
    if not response.ok:
        setup.logger.error(response)
    return response.json()


def get_src(url):
    """Функция возвращает временную ссылку на скачивание фотографии без авторизации
    Ссогласно документации МойСклад, ссылка действительна в течение 1 минуты.
    """
    headers = {
        'Authorization': f'Bearer {MOYSKLAD_TOKEN}'
    }
    response = requests.request("GET", url, headers=headers)
    if not response.ok:
        setup.logger.error(response)
    return response.url


if __name__ == '__main__':
    get_goods()
