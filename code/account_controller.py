import bcrypt

from connector import get_db
from support import get_current_time


class AccountController:

    def login(self, user_name, password):
        login_sql = "SELECT * FROM account WHERE username = '{}'".format(user_name)
        db = get_db()
        cursor = db.cursor()
        cursor.execute(login_sql)
        account = cursor.fetchone()
        db.commit()
        db.close()
        if account is None: return "Account not existed"
        is_password_match = bcrypt.checkpw(password.encode('utf-8'), account[1].encode('utf-8'))
        if not is_password_match: return "Password is incorrect"
        with open('../account.txt', 'w') as file:
            file.write(user_name + "\n" + account[1])
        return None

    def check_cache_login(self):
        try:
            with open('../account.txt', 'r') as file:
                user_name = file.readline().rstrip()
                pass_word = file.readline().rstrip()
            login_sql = "SELECT * FROM account WHERE username = '{}'".format(user_name)
            db = get_db()
            cursor = db.cursor()
            cursor.execute(login_sql)
            account = cursor.fetchone()
            db.commit()
            db.close()
            if account is None: return None
            is_password_match = pass_word.encode('utf-8') == account[1].encode('utf-8')
            if not is_password_match: return None
            return user_name
        except:
            return None

    def register(self, user_name, password):
        check_exist_sql = "SELECT COUNT('username') FROM account WHERE username = '{}'".format(user_name)
        db = get_db()
        cursor = db.cursor()
        cursor.execute(check_exist_sql)
        count = cursor.fetchone()[0]
        if count > 0:
            return "Account existed"
        timestamp = get_current_time()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        register_sql = "INSERT INTO account(username, password,create_date,update_date) VALUES ('{}', '{}', '{}', '{}')".format(
            user_name,
            hashed_password.decode('utf-8'),
            timestamp, timestamp)
        cursor.execute(register_sql)
        db.commit()
        db.close()
        return None
