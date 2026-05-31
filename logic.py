import sqlite3
from config import DATABASE


class DB_Manager:
    def __init__(self, database):
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.database)
        return self.connection

    def create_tables(self):
        conn = self.connect()
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    number INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price TEXT NOT NULL,
                    link TEXT DEFAULT NULL
                )
            ''')

    def insert_data(self, table, data):
        conn = self.connect()
        placeholders = ', '.join(['?' for _ in data[0]])
        columns = ', '.join(data[0].keys())
        sql = f'INSERT OR IGNORE INTO {table} ({columns}) VALUES ({placeholders})'
        with conn:
            conn.executemany(sql, [tuple(row.values()) for row in data])
            conn.commit()

    def select_data(self, sql, params=()):
        conn = self.connect()
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(sql, params)
                return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []

    def update_data(self, table, set_clause, where_clause, params):
        conn = self.connect()
        sql = f'UPDATE {table} SET {set_clause} WHERE {where_clause}'
        with conn:
            conn.execute(sql, params)
            conn.commit()

    def delete_data(self, table, where_clause, params):
        conn = self.connect()
        sql = f'DELETE FROM {table} WHERE {where_clause}'
        with conn:
            conn.execute(sql, params)
            conn.commit()

    def get_all_products(self):
        """Возвращает все товары: (number, name, price, link)."""
        return self.select_data("SELECT number, name, price, link FROM users ORDER BY name")

    def search_products(self, query):
        """Ищет товары по части названия."""
        return self.select_data(
            "SELECT number, name, price, link FROM users WHERE name LIKE ?",
            (f'%{query}%',)
        )

    def get_product_by_id(self, product_id):
        """Возвращает один товар по ID."""
        result = self.select_data(
            "SELECT number, name, price, link FROM users WHERE number = ?",
            (product_id,)
        )
        return result[0] if result else None

    def close(self):
        if self.connection:
            self.connection.close()


# ─── Первичная инициализация БД и наполнение данными ───────────────────────

products_to_add = [
    {'name': 'Кружка геншин мика', 'price': '356', 'link': 'https://www.wildberries.ru/catalog/471223521/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин невиллет', 'price': '508', 'link': 'https://www.wildberries.ru/catalog/493447757/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин оророн', 'price': '652', 'link': 'https://www.wildberries.ru/catalog/420807573/detail.aspx?targetUrl=SN0'},
    {'name': 'Кружка геншин ризли', 'price': '207', 'link': 'https://www.wildberries.ru/catalog/14188355/detail.aspx?targetUrl=SN0'},
    {'name': 'Кружка геншин рейзор', 'price': '118', 'link': 'https://www.wildberries.ru/catalog/100339569/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин венти', 'price': '548', 'link': 'https://www.wildberries.ru/catalog/145759837/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин чжун ли', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/198641396/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин дилюк', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/198642236/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кейа', 'price': '439', 'link': 'https://www.wildberries.ru/catalog/38167202/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин итэр', 'price': '418', 'link': 'https://www.wildberries.ru/catalog/313096631/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин альбедо', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341808/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин Варка', 'price': '410', 'link': 'https://www.wildberries.ru/catalog/817222720/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин аято', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341807/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин бай чжу', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341817/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин беннет', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009704739/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин горо', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341814/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин далья', 'price': '446', 'link': 'https://www.wildberries.ru/catalog/834388265/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин дурин', 'price': '302', 'link': 'https://www.wildberries.ru/catalog/740465816/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин иллуги', 'price': '374', 'link': 'https://www.wildberries.ru/catalog/837726478/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин итто', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211679545/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ифа', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/444721711/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кавех', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341813/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ка мин', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680027/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кадзуха', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680028/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кинич', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/444721719/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин лини', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009704755/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин лоэн', 'price': '434', 'link': 'https://www.wildberries.ru/catalog/969506386/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сайно', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341824/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сетос', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1021554777/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин син цю', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341825/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин скарамуча', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680860/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сяо', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/198639922/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин тарталья', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/198596680/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин тигнари', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680862/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин тома', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009736577/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин флинс', 'price': '388', 'link': 'https://www.wildberries.ru/catalog/548980870/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин фремине', 'price': '574', 'link': 'https://www.wildberries.ru/catalog/330514649/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин хейдзо', 'price': '156', 'link': 'https://www.wildberries.ru/catalog/214344077/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин чунь юнь', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214344087/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин яэ мико', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211681633/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин яо яо', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009736578/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин янь фей', 'price': '439', 'link': 'https://www.wildberries.ru/catalog/44466930/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ягода', 'price': '569', 'link': 'https://www.wildberries.ru/catalog/835800225/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин юнь цзынь', 'price': '294', 'link': 'https://www.wildberries.ru/catalog/59751706/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин эскофье', 'price': '678', 'link': 'https://www.wildberries.ru/catalog/695281592/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин эола', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009615204/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин эмилия', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/275009442/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин эмбер', 'price': '237', 'link': 'https://www.wildberries.ru/catalog/224734771/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин элой', 'price': '349', 'link': 'https://www.wildberries.ru/catalog/660048972/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин шень хе', 'price': '381', 'link': 'https://www.wildberries.ru/catalog/182010385/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин шилонен', 'price': '329', 'link': 'https://www.wildberries.ru/catalog/1021554791/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин шеврёз', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211681632/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин шарлота', 'price': '381', 'link': 'https://www.wildberries.ru/catalog/192276513/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин часка', 'price': '246', 'link': 'https://www.wildberries.ru/catalog/264997130/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ци ци', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211681631/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин цзы бай', 'price': '369', 'link': 'https://www.wildberries.ru/catalog/817279884/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ху тао', 'price': '210', 'link': 'https://www.wildberries.ru/catalog/198647019/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин фурина', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211681630/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин фишль', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214344076/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин фарузан', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214344084/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин тиори', 'price': '402', 'link': 'https://www.wildberries.ru/catalog/227972050/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сянь юнь', 'price': '402', 'link': 'https://www.wildberries.ru/catalog/227972059/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сян лин', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214344078/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин скирк', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/337356093/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ситлали', 'price': '506', 'link': 'https://www.wildberries.ru/catalog/315670340/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин син янь', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680861/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин синобу', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680031/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сиджвин', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1021554779/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин саю', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214342213/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сахароза', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214344074/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сара', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009736579/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин сандроне', 'price': '369', 'link': 'https://www.wildberries.ru/catalog/817732991/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин розария', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214344080/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин райден', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/198642706/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин феофан', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1021554776/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ноэль', 'price': '300', 'link': 'https://www.wildberries.ru/catalog/59751704/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин нин гуан', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214344079/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин нилу', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341826/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин николь', 'price': '302', 'link': 'https://www.wildberries.ru/catalog/817550242/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин нефер', 'price': '751', 'link': 'https://www.wildberries.ru/catalog/611637349/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин нахида', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/198592635/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин навия', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680855/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин муалани', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/444721729/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин мона', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680854/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин мидзуки', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/337356092/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин мавуика', 'price': '402', 'link': 'https://www.wildberries.ru/catalog/316728530/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин линнея', 'price': '466', 'link': 'https://www.wildberries.ru/catalog/1036374802/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин линетт', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009736591/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин лиза', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341822/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин лаума', 'price': '506', 'link': 'https://www.wildberries.ru/catalog/547333495/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин лань янь', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/328611454/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин лайла', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214342209/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кэ цин', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341820/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин коломбина', 'price': '410', 'link': 'https://www.wildberries.ru/catalog/740430912/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кокоми', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211680030/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин клоринда', 'price': '506', 'link': 'https://www.wildberries.ru/catalog/238472355/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кли', 'price': '439', 'link': 'https://www.wildberries.ru/catalog/38167206/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кирара', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341818/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин качина', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/1021665644/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин кандакия', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341819/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин инеффа', 'price': '506', 'link': 'https://www.wildberries.ru/catalog/490097974/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин иансан', 'price': '506', 'link': 'https://www.wildberries.ru/catalog/397800908/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин ёимия', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211679544/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин е лань', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211679543/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин дехья', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211679542/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин дори', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341811/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин диона', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341809/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин джинн', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341812/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин гань юй', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211678999/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин вареса', 'price': '400', 'link': 'https://www.wildberries.ru/catalog/444721705/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин бей доу', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341815/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин барбара', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341806/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин аяка', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/211677312/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин арлекино', 'price': '385', 'link': 'https://www.wildberries.ru/catalog/444721704/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин айно', 'price': '506', 'link': 'https://www.wildberries.ru/catalog/547338653/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин коллеи', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341823/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин аль хайтам', 'price': '216', 'link': 'https://www.wildberries.ru/catalog/214341810/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин дайнслейф', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009704740/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин паймон', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009704742/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин дотторе', 'price': '320', 'link': 'https://www.wildberries.ru/catalog/1009704743/detail.aspx?targetUrl=SN'},
    {'name': 'Кружка геншин рерир', 'price': '434', 'link': 'https://www.wildberries.ru/catalog/554652080/detail.aspx?targetUrl=SN'},
]


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    try:
        manager.insert_data('users', products_to_add)
        print("Товары успешно добавлены!")
    except Exception as e:
        print(f"Ошибка: {e}")

    result = manager.get_all_products()
    for row in result:
        print(row)

    manager.close()

