from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup


class Buttons:
    cancel_text = "❌ Отмена"
    terms_text = "📄 Условия конкурса"
    schedule_text = "📅 Сроки проведения"
    prizes_text = "🏆 Призы"
    help_text = "❓ Помощь"
    send_work = "🎨 Отправить работу"

    @property
    def cancel_button(self):
        return ReplyKeyboardMarkup(
            [[KeyboardButton(self.cancel_text)]], resize_keyboard=True
        )

    @property
    def main_menu(self):
        return ReplyKeyboardMarkup(
            [
                [KeyboardButton(self.send_work)],
                [
                    KeyboardButton(self.terms_text),
                    KeyboardButton(self.schedule_text),
                ],
                [
                    KeyboardButton(self.prizes_text),
                    KeyboardButton(self.help_text),
                ],
            ],
            resize_keyboard=True,
        )


buttons = Buttons()
