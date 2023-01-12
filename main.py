import moysklad
import insales
import setup


def set_images(ms_code, ins_code):
    """Базовая функция: получает на вход код товара в МС и Инсейлз,
    получает временные ссылки на скачивание фото из МС и отправляет
    их в Инсейлз.
    """
    images = moysklad.get_images(ms_code)
    for each in images['rows']:
        url = each['meta']['downloadHref']
        src = moysklad.get_src(url)
        insales.put_image(ins_code, src)


if __name__ == '__main__':
    setup.logger.debug("получаем из МойСклад товары, у которых есть фото и формируем словарь вида {внешний код: код МойСклад}")
    ms_goods = moysklad.get_goods()
    setup.logger.debug("получаем товары из InSales, у которых нет фото, и формируем словарь вида {внешний код: код InSales}")
    ins_goods = insales.get_goods()
    setup.logger.debug("Запускаем основную функцию")
    for i in ms_goods:
        try:
            ins_code = ins_goods[i]
            set_images(ms_goods[i], ins_goods[i])
        except KeyError:
            pass
