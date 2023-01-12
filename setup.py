import logging

DEBUG = False  # set True to save debug files in ./temp

INSALES_BASE_URL = 'https://myshop-47483-27.myinsales.ru/admin'
INSALES_API_ID = 'api_id'
INSALES_API_PASS = 'api_password'
INSALES_PER_PAGE: int = 250

MOYSKLAD_NAME = 'moysklad_username'
MOYSKLAD_SECRET = 'moysklad_password'
MOYSKLAD_BASE_URL = 'https://online.moysklad.ru/api/remap/1.2'
MOYSKLAD_TOKEN = 'moy-sklad-token'
MOYSKLAD_PER_PAGE: int = 250

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
