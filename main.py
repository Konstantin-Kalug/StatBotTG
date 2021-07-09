from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from plot import Plot


START_MARKUP = [['Создать диаграмму', 'Настроить диаграмму'], ['/help', '/stop']]
BACK_MARKUP = [['Вернуться назад'], ['/stop']]
COLORS_MARKUP = [['Любые'], ['Вернуться назад'], ['/stop']]
SETTINGS_MARKUP = [['Title: '], ['XLabel: '], ['YLabel: '], ['Color: '],
                   ['Type: '], ['Legend: '], ['Вернуться назад'], ['/stop']]
HELP_ADDRESS = 'static/txt/help.txt'
FIGURE_ADDRESS = 'static/img/figure.png'


class Bot:
    def __init__(self):
        # инициализация бота
        TOKEN = ''
        updater = Updater(TOKEN, use_context=True)
        # работа с телеграммом
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start, pass_user_data=True)],
            states={
                1: [CommandHandler('stop', self.stop), CommandHandler('help', self.help),
                    MessageHandler(Filters.text, self.start_text_handler_func,
                                   pass_user_data=True)],
                2: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.create_text_handler_func,
                                   pass_user_data=True)],
                3: [CommandHandler('stop', self.stop),
                    MessageHandler(Filters.text, self.setting_text_handler_func,
                                   pass_user_data=True)]
            },
            fallbacks=[CommandHandler('stop', self.stop)]
        )
        dp.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()

    def create_keyboard(self, markup):
        return ReplyKeyboardMarkup(markup, one_time_keyboard=False)

    def close_keyboard(self, update, context):
        # скрываем клавиатуру
        update.message.reply_text(
            "Увидимся позже!",
            reply_markup=ReplyKeyboardRemove()
        )

    def start(self, update, context):
        update.message.reply_text('Приветствую, с помощью этого бота вы можете создавать диаграммы!'
                                  ' Советую использовать кнопки!',
                                  reply_markup=self.create_keyboard(START_MARKUP))
        context.user_data['title'] = ''
        context.user_data['color'] = 'Любые'
        context.user_data['xlabel'] = ''
        context.user_data['ylabel'] = ''
        context.user_data['type'] = 'Столбчатая'
        context.user_data['legend'] = False
        context.user_data['info'] = ''
        return 1

    def stop(self, update, context):
        # завершаем работу бота
        self.close_keyboard(update, context)
        return ConversationHandler.END

    def help(self, update, context):
        with open(HELP_ADDRESS, 'r', encoding='utf-8') as f:
            update.message.reply_text('\n'.join(f.readlines()),
                                      reply_markup=self.create_keyboard(START_MARKUP))
            return 1

    def start_text_handler_func(self, update, context):
        if update.message.text == 'Создать диаграмму':
            update.message.reply_text('Отправьте данные одним сообщением!',
                                      reply_markup=self.create_keyboard(BACK_MARKUP))
            return 2
        elif update.message.text == 'Настроить диаграмму':
            markup = SETTINGS_MARKUP
            markup[0][0] += context.user_data['title']
            markup[1][0] += context.user_data['xlabel']
            markup[2][0] += context.user_data['ylabel']
            markup[3][0] += context.user_data['color']
            markup[4][0] += context.user_data['type']
            markup[5][0] += context.user_data['legend']
            update.message.reply_text('Настройте будущую диаграмму!',
                                      reply_markup=self.create_keyboard(markup))
            return 3
        else:
            update.message.reply_text('Используйте кнопки, пожалуйста!',
                                      reply_markup=self.create_keyboard(START_MARKUP))

    def create_text_handler_func(self, update, context):
        if update.message.text == 'Вернуться назад':
            return 1
        else:
            plot = Plot(context.user_data['title'], context.user_data['xlabel'],
                        context.user_data['ylabel'], context.user_data['color'],
                        context.user_data['type'], context.user_data['legend'], update.message.text)
            if plot.create_figure(FIGURE_ADDRESS) is None:
                self.send_img(FIGURE_ADDRESS, context, update, 'Вот ваша диаграмма!')
                return 2
            else:
                update.message.reply_text('Используйте кнопки!',
                                          reply_markup=self.create_keyboard(BACK_MARKUP))
                return 2

    def setting_text_handler_func(self, update, context):
        pass

    def send_img(self, address, context, update, text):
        try:
            context.bot.send_photo(
                update.message.chat_id,
                open(address, 'rb'),
                caption=text
            )
        except Exception:
            update.message.reply_text('Возникла ошибка!',
                                      reply_markup=self.create_keyboard(BACK_MARKUP))


if __name__ == '__main__':
    bot = Bot()
