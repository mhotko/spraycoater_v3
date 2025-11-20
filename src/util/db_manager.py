import sqlite3


class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=(), commit=True) -> sqlite3.Cursor:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            return cursor

    def query_all(self, sql: str, params=()) -> list[tuple]:
        cursor = self.execute_query(sql, params, commit=False)
        return cursor.fetchall()

    def query_one(self, sql: str, params=()) -> tuple[str] | None:
        cursor = self.execute_query(sql, params, commit=False)
        return cursor.fetchone()

    def update(self, table: str, key: str, value: str) -> None:
        self.execute_query(
            f"UPDATE {table} SET value=? WHERE key=?", (value, key)
        )
