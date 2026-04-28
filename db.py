import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `Users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = (str(row[0]))
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id))

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = (str(row[0]))
            return nickname

    def add_phone(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `Users` (`phone`) VALUES (?)", (user_id,))

    def set_phone(self, user_id, phone):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `phone` = ? WHERE `user_id` = ?", (phone, user_id,))

    def get_phone(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `phone` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                phone = (str(row[0]))
            return phone

    def phone_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_user_token(self, user_id, user_token):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `user_token` = ? WHERE `user_id` = ?", (user_token, user_id,))

    def get_user_token(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `user_token` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                token_id = (str(row[0]))
            return token_id

    def set_phone_code(self, user_id, phone_code):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `phone_code` = ? WHERE `user_id` = ?", (phone_code, user_id,))

    def get_phone_code(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `phone_code` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                code = (str(row[0]))
            return code

    def phone_code_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_auth_token(self, user_id, auth_token):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `auth_token` = ? WHERE `user_id` = ?", (auth_token, user_id,))

    def get_auth_token(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `auth_token` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                token = (str(row[0]))
            return token

    def set_supplier(self, user_id, supplier):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `supplier` = ? WHERE `user_id` = ?", (supplier, user_id,))

    def get_supplier(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `supplier` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                token = (str(row[0]))
            return token

    def delete_user(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM `Users` WHERE `user_id` = ?", (user_id,))

    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                times = (str(row[0]))
            return times

    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                times = int(row[0])
            if times > int(time.time()):
                return True
            else:
                return False

    def set_time_token(self, user_id, time_token):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `time_token` = ? WHERE `user_id` = ?", (time_token, user_id,))

    def set_date_now(self, user_id, date_now):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `date_now` = ? WHERE `user_id` = ?", (date_now, user_id,))

    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id,))

    def get_date_now(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `date_now` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                times = (str(row[0]))
            return times

    def get_otz_count(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `otz_count` FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                otz = (str(row[0]))
            return otz

    def set_otz_count(self, user_id, otz_count):
        with self.connection:
            self.cursor.execute("UPDATE `Users` SET `otz_count` = ? WHERE `user_id` = ?", (otz_count, user_id,))
