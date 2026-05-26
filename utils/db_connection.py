import os
import pymysql
import pymysql.cursors

conn: pymysql.connections.Connection[pymysql.cursors.DictCursor] | None = None


def get_connection() -> pymysql.connections.Connection[pymysql.cursors.DictCursor]:
    global conn
    if conn is None or not conn.open:
        conn = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.environ["DB_PORT"]),
        read_timeout=5,
        write_timeout=5,
    )
    assert conn is not None
    return conn