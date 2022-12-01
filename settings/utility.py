def _convert(list_convert):
    return [item[0] for item in list_convert]


def get_total_cost(DB):
    """
    Возвращает общую стоимость товара
    """
    all_product_id = DB.select_all_product_id()
    all_price = [DB.select_single_product_price(item)
                 for item in all_product_id]
    all_quantity = [DB.select_order_quantity(item)
                    for item in all_product_id]
    return total_cost(all_quantity, all_price)


def total_cost(list_quantity, list_price):
    """
    Считает общую сумму заказа и возвращает результат
    """
    order_total_cost = 0
    for ind, itm in enumerate(list_price):
        order_total_cost += list_quantity[ind] * list_price[ind]
    return order_total_cost


def total_quantity(list_quantity):
    """
    Считает общее количество заказанной единицы товара и возвращает результат
    """
    order_total_quantity = 0
    for itm in list_quantity:
        order_total_quantity += itm
    return order_total_quantity


def get_total_quantity(DB):
    """
    Возвращает общее количество заказанной единицы товара
    """
    all_product_id = DB.select_all_product_id()
    all_quantity = [DB.select_order_quantity(itm)
                    for itm in all_product_id]
    return total_quantity(all_quantity)
