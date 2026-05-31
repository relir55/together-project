import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN, DATABASE
from logic import DB_Manager, products_to_add

# ─── Логирование ────────────────────────────────────────────────────────────

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── Инициализация ───────────────────────────────────────────────────────────

bot = telebot.TeleBot(TOKEN)
db = DB_Manager(DATABASE)

# Создаём таблицы и наполняем БД при первом запуске
db.create_tables()
db.insert_data('users', products_to_add)

# ─── Вспомогательные функции ─────────────────────────────────────────────────

PRODUCTS_PER_PAGE = 10


def build_product_text(row):
    """Формирует текст одного товара: (id, name, price, link)."""
    number, name, price, link = row
    return f"📦 *{name}*\n💰 Цена: {price.strip()} руб.\n🔗 [Купить на Wildberries]({link})"


def build_catalog_keyboard(products, page, total_pages):
    """Инлайн-клавиатура со списком товаров и навигацией."""
    keyboard = InlineKeyboardMarkup(row_width=1)

    for number, name, price, link in products:
        keyboard.add(InlineKeyboardButton(
            text=f"{name} — {price.strip()} руб.",
            callback_data=f"product_{number}"
        ))

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Назад", callback_data=f"page_{page - 1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Вперёд ▶️", callback_data=f"page_{page + 1}"))

    if nav_buttons:
        keyboard.row(*nav_buttons)

    return keyboard


def get_page(page: int):
    """Возвращает товары и клавиатуру для нужной страницы."""
    all_products = db.get_all_products()
    total = len(all_products)
    total_pages = max(1, (total + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE)
    page = max(0, min(page, total_pages - 1))

    start = page * PRODUCTS_PER_PAGE
    chunk = all_products[start:start + PRODUCTS_PER_PAGE]

    text = f"🛍️ *Каталог кружек Геншин* (стр. {page + 1}/{total_pages})\nВыбери товар:"
    keyboard = build_catalog_keyboard(chunk, page, total_pages)
    return text, keyboard


# ─── Обработчики команд ──────────────────────────────────────────────────────

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        f"Привет, *{message.from_user.first_name}*! 👋\n\n"
        "Я помогу тебе найти кружку из Геншин Импакт.\n\n"
        "📋 /catalog — просмотреть весь каталог\n"
        "🔍 /search — найти товар по имени персонажа\n"
        "❓ /help — помощь",
        parse_mode='Markdown'
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(
        message,
        "📖 *Доступные команды:*\n\n"
        "/start — начать работу с ботом\n"
        "/catalog — открыть каталог товаров\n"
        "/search — найти товар по имени персонажа\n"
        "/help — эта справка",
        parse_mode='Markdown'
    )


@bot.message_handler(commands=['catalog'])
def catalog(message):
    text, keyboard = get_page(0)
    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')


@bot.message_handler(commands=['search'])
def search_prompt(message):
    msg = bot.reply_to(message, "🔍 Введи имя персонажа для поиска:")
    bot.register_next_step_handler(msg, search_result)


def search_result(message):
    query = message.text.strip()
    results = db.search_products(query)

    if not results:
        bot.reply_to(message, f"😔 По запросу *«{query}»* ничего не найдено.", parse_mode='Markdown')
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for number, name, price, link in results[:20]:
        keyboard.add(InlineKeyboardButton(
            text=f"{name} — {price.strip()} руб.",
            callback_data=f"product_{number}"
        ))

    bot.send_message(
        message.chat.id,
        f"🔍 Результаты по запросу *«{query}»* ({len(results)} шт.):",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )


# ─── Обработчики callback-кнопок ─────────────────────────────────────────────

@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def handle_page(call):
    page = int(call.data.split('_')[1])
    text, keyboard = get_page(page)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def handle_product(call):
    product_id = int(call.data.split('_')[1])
    row = db.get_product_by_id(product_id)

    if not row:
        bot.answer_callback_query(call.id, "Товар не найден.")
        return

    text = build_product_text(row)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔗 Открыть на Wildberries", url=row[3]))
    keyboard.add(InlineKeyboardButton("◀️ Вернуться в каталог", callback_data="page_0"))

    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=keyboard,
        parse_mode='Markdown',
        disable_web_page_preview=False
    )
    bot.answer_callback_query(call.id)


# ─── Запуск ──────────────────────────────────────────────────────────────────

def main():
    logger.info("Бот запущен...")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
