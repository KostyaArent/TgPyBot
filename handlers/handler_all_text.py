from settings.message import MESSAGES
from settings import config, utility
from handlers.handler import Handler


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        self.step = 0

    def pressed_btn_info(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_category(self, message):
        self.bot.send_message(message.chat.id, "Меню",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Выберите категорию",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_product(self, message, product):
        self.bot.send_message(message.chat.id, "Категория" + config.KEYBOARD[product],
                              reply_markup=self.keybords.select_set_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Done",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):
        self.step = 0
        count = self.DB.select_all_product_id()
        quantity = self.DB.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_up(self, message):
        """
        Обработка нажатия кнопки увеличения
        количества определенного товара в заказе
        """
        count = self.DB.select_all_product_id()
        quantity_order = self.DB.select_order_quantity(count[self.step])
        quantity_product = self.DB.select_single_product_quantity(
            count[self.step])
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            self.DB.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            self.DB.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        """
        Обработка нажатия кнопки уменьшения
        количества определенного товара в заказе
        """
        count = self.DB.select_all_product_id()
        quantity_order = self.DB.select_order_quantity(count[self.step])
        quantity_product = self.DB.select_single_product_quantity(
            count[self.step])
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            self.DB.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            self.DB.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """
        Обрабатывает нажатие кнопки удаления товара в заказе
        """
        count = self.DB.select_all_product_id()

        if count.__len__() > 0:
            quantity_order = self.DB.select_order_quantity(count[self.step])
            quantity_product = self.DB.select_single_product_quantity(
                count[self.step])
            quantity_product += quantity_order
            self.DB.delete_order(count[self.step])
            self.DB.update_product_value(count[self.step], 'quantity',
                                         quantity_product)
            if self.step != 0:
                self.step -= 1
        count = self.DB.select_all_product_id()

        if count.__len__() > 0:
            quantity_order = self.DB.select_order_quantity(count[self.step])
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        """
        Обрабатывает нажатие кнопки перемещения
        на предыдущую позицию товара в заказе
        """
        if self.step > 0:
            self.step -= 1
        count = self.DB.select_all_product_id()
        quantity = self.DB.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        """
        Обрабатывает нажатие кнопки перемещения
        на следующую позицию товара в заказе
        """
        if self.step < self.DB.count_rows_order() - 1:
            self.step += 1
        count = self.DB.select_all_product_id()
        quantity = self.DB.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apply(self, message):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'Оформить заказ'.
        """
        self.bot.send_message(message.chat.id,
                              MESSAGES['apply'].format(
                                  utility.get_total_cost(self.DB),
                                  utility.get_total_quantity(self.DB)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.category_menu())
        self.DB.delete_all_order()

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step + 1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.DB.select_single_product_category(
                                    product_id),
                                  self.DB.select_single_product_name(
                                      product_id),
                                  self.DB.select_single_product_title(
                                      product_id),
                                  self.DB.select_single_product_price(
                                      product_id),
                                  self.DB.select_order_quantity(
                                      product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(
                                  self.step, quantity))

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['ORDER']:
                if self.DB.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.category_menu())

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            # Управление заказом
            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOWN']:
                self.pressed_btn_down(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLY']:
                self.pressed_btn_apply(message)

            # Меню, пицца, мороженное, кофе
            if message.text == config.KEYBOARD['PIZZA']:
                self.pressed_btn_product(message, 'PIZZA')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            if message.text == config.KEYBOARD['COFFEE']:
                self.pressed_btn_product(message, 'COFFEE')

            # Если команда не распознана
            else:
                self.bot.send_message(message.chat.id, message.text)
