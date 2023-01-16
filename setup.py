import logging
import json

DEBUG = True  # set True to save debug files in FILEDIR
FILEDIR = 'temp'

INSALES_BASE_URL = 'https://myshop-bla-bla.myinsales.ru/admin'
INSALES_API_ID = 'insales-api-id'
INSALES_API_PASS = 'insales-api-password'
INSALES_PER_PAGE: int = 250

MOYSKLAD_NAME = 'moysklad_username'
MOYSKLAD_SECRET = 'moysklad_password'
MOYSKLAD_BASE_URL = 'https://online.moysklad.ru/api/remap/1.2'
MOYSKLAD_TOKEN = 'moysklad-token'
MOYSKLAD_PER_PAGE: int = 250


def save_debug_file(filename, data):
    with open(f'{FILEDIR}/{filename}', 'w+', encoding='utf8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Logging setup
# Change fh.setLevel from ERROR to DEBUG when tracing issues

# create logger
logger = logging.getLogger('moysklad-insales')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages (set to 'error' when ran in production)
fh = logging.FileHandler('temp/moysklad-insales.log')
fh.setLevel(logging.ERROR)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
