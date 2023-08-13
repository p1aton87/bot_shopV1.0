import sqlite3 as sl

price_connect = sl.connect('price.db')
with price_connect:
    select_all_items = price_connect.execute('SELECT * FROM price_table')
    all_information = select_all_items.fetchall()

    def check(self, inter):
        select_one_items = price_connect.execute('SELECT name_item, link, cost_usd FROM price_table WHERE articul = ?', [self])
        check_one = select_one_items.fetchone()[inter]
        return check_one

userdb_connect = sl.connect('users.db')
cursor = userdb_connect.cursor()
with userdb_connect:
    def update_users(self):
        update = cursor.execute('UPDATE user_table SET pay_or_not = "paid/оплачено" WHERE id = ? AND _ROWID_ = (SELECT _ROWID_ FROM user_table WHERE id = ? ORDER BY _ROWID_ DESC LIMIT 1)',
                                [self, self])
        userdb_connect.commit()


    def add_user(id, username, articul_id):
        add_all_items = cursor.execute('INSERT INTO user_table (id, username, articul_items, pay_or_not) VALUES (?, ?, ?, ?)', [id, username, articul_id, 'not paid/не оплачено'])
        userdb_connect.commit()

    def check_all_items(self):
        check_items = cursor.execute('SELECT * FROM user_table where id = (?) AND pay_or_not = "paid/оплачено"', [self])
        order = check_items.fetchall()
        return order

    def delete_no_payed_items(self):
        cursor.execute('DELETE FROM user_table WHERE id = ? AND pay_or_not = "not paid/не оплачено"', [self])
        userdb_connect.commit()



