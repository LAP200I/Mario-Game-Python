from connector import get_db
from support import get_current_time


class GameDataController:
    def __init__(self):
        pass

    def create_game_data(self, user_name):
        db = get_db()
        cursor = db.cursor()
        time_stamp = get_current_time()
        insert_game_data_sql = "INSERT INTO gamedata (username, create_date, update_date) VALUES ('{}', '{}', '{}')".format(
            user_name, time_stamp, time_stamp)
        cursor.execute(insert_game_data_sql)
        db.commit()
        db.close()

    def get_game_data(self, user_name):
        db = get_db()
        cursor = db.cursor()
        insert_game_data_sql = "SELECT * FROM gamedata WHERE username = '{}'".format(user_name)
        cursor.execute(insert_game_data_sql)
        rs = cursor.fetchone()
        db.commit()
        db.close()
        return rs

    def update_coin(self, user_name, new_coin):
        db = get_db()
        cursor = db.cursor()
        time_stamp = get_current_time()
        update_coin_sql = "UPDATE gamedata SET coin = '{}', update_date= '{}' WHERE username = '{}'".format(
            new_coin, time_stamp, user_name)
        cursor.execute(update_coin_sql)
        db.commit()
        db.close()

    def update_next_level(self, user_name, new_max_level):
        db = get_db()
        cursor = db.cursor()
        time_stamp = get_current_time()
        update_level_sql = "UPDATE gamedata SET level = '{}', update_date= '{}' WHERE username = '{}'".format(
            new_max_level, time_stamp, user_name)
        cursor.execute(update_level_sql)
        db.commit()
        db.close()
