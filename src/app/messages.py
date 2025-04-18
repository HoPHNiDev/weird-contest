from src.app.config import settings, DATE_FORMAT
from src.app.models import User, Works

welcome_text = f"""Привет, дорогой участник!
Ты попал в бот конкурса на лучший рисунок/дизайн для проекта YourFit!

YourFit — это российский бренд качественного инвентаря для фитнеса, который выбирают уже более 1 000 000 клиентов.
- Входим в 1000 брендов WB
- 2 место на Ozon в спорте
- Дружная команда профессионалов
Наша миссия — сделать спорт доступным каждому!
Мы искренне верим и делаем всё, чтобы спорт приносил не только здоровье, но и эстетическое удовольствие 😻

🎨 Что нужно сотворить?
- Создать оригинальный рисунок/дизайн для коврика
- Отправить его через этого бота до 20.05.2025
🏆 Главный приз: 50,000 ₽ + сертификат на продукцию YourFit

Выбери действие в меню ниже 👇🏻"""

terms_text = """📌 Правила участия:

✅ Работа должна быть уникальной (не скопированной)
✅ Формат: JPG/PNG/SVG, не более 5 МБ
✅ Тема: Идеальный принт для коврика йоги
✅ Один участник — до 10 вариантов работ

🚫 Запрещено:
- Использовать чужие работы (плагиат)
- Нарушать авторские права
- Отправлять оскорбительный контент

Полное ТЗ >>[здесь](https://telegra.ph/Tehnicheskoe-zadanie-04-15)<<

❓ Есть вопросы? Напиши /help
"""

schedule_text = f"""📅 Сроки проведения:

• Начало: {settings.COMPETITION_START.strftime(DATE_FORMAT)}
• Окончание приема работ: {settings.COMPETITION_END.strftime(DATE_FORMAT)}
• Объявление результатов: {settings.RESULTS_DATE.strftime(DATE_FORMAT)}"""

prizes_text = """🏆 Призовой фонд:

1 место: 50,000 ₽ + сертификат на продукцию YourFit
2 место: 15,000 ₽ + сертификат на продукцию YourFit 
3 место: 10,000 ₽ + сертификат на продукцию YourFit 

➕ Дополнительные номинации: 
👨‍🎨 Самый оригинальный концепт
🧝‍♀️ Приз зрительских симпатий
"""

help_text = f"""❓ Частые вопросы:

🔹 Можно ли отредактировать работу после отправки?
— Пришлите комментарий с номером заявки (@yourfitgo)

🔹 Как определяется победитель?
— Голосование жюри + народное голосование

🔹 Когда объявят результаты?
— {settings.RESULTS_DATE.strftime(DATE_FORMAT)}, следите за нашим каналом

📩 Другие вопросы? Пишите @yourfitgo"""

about_us_text = """
YourFit — это российский бренд качественного инвентаря для фитнеса, который выбирают уже более 1 000 000 клиентов.

- Входим в 1000 брендов WB
- 2 место на Ozon в спорте
- Дружная команда профессионалов
Наша миссия — сделать спорт доступным каждому!

Мы искренне верим и делаем всё, чтобы спорт приносил не только здоровье, но и эстетическое удовольствие 😻
"""

send_work_media = """🖌️ Пришли фото/файл своего рисунка/дизайна:\n\n
Форматы: JPG/PNG/SVG, не более 5 МБ"""

send_work_text = """📝 Теперь добавь описание и контакты:\n
- Название работы\n
- Краткое описание (по желанию)\n
- Контакты (Telegram/email)\n\n"""

timeout_text = "⏰ Время ожидания истекло. Попробуйте снова."

max_work_sent = "❌ Вы уже отправили максимальное количество работ."

unknown_command = "❌ Неизвестная команда. Попробуйте снова."

main_menu = "🏘 Главное меню..."


def new_work_msg(user: User, description: str, work: Works | None = None):
    msg = f"""
Новый участник конкурса! 🎉
Telegram ID: {user.tg_id}
Username: @{user.username}
"""
    if work:
        msg += f"""
Номер заявки: {work.id}
Ссылка на работу: {work.work_link}
"""

    msg += f"""
```Описание работы: 
{description}
```
"""
    return msg


def success_work_msg(work: Works):
    return f"""✅ Ваша работа успешно отправлена на конкурс!

Номер вашей заявки: {work.id}

За ходом развития нашего конкурса и итоговых результатов голосования можно следить на нашем основном канале: https://t.me/yourfit_store
"""
