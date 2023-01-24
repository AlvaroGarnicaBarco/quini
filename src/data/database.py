import psycopg2


class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def __enter__(self):
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    def select(self, table, columns='*', where=None):
        query = f"SELECT {columns} FROM {table}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, table, values):
        query = f"INSERT INTO {table} VALUES {values}"
        self.cursor.execute(query)
        self.connection.commit()

    def update(self, table, set_values, where):
        query = f"UPDATE {table} SET {set_values} WHERE {where}"
        self.cursor.execute(query)
        self.connection.commit()

    def delete(self, table, where):
        query = f"DELETE FROM {table} WHERE {where}"
        self.cursor.execute(query)
        self.connection.commit()


if __name__ == "__main__":
    with Database(host='localhost', database='mydb', user='myuser', password='mypassword') as db:
        db.insert('users', "(1, 'John', 'Doe', 'johndoe@example.com')")
        users = db.select('users')
        for user_ in users:
            print(user_)

