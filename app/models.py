
class Database:
    
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def execute_read_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        if self.cursor.with_rows:
            return self.cursor.fetchall()

    def execute_write_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def execute_update_query(self, query, params=None):
        self.execute_write_query(query, params)

    def execute_delete_query(self, query, params=None):
        self.execute_write_query(query, params) 

    def fetch_all(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

