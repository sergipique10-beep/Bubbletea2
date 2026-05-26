import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=10,
    cursorclass=pymysql.cursors.DictCursor,
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
    port=int(os.environ["DB_PORT"]),
)

with conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bubble_teas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                temperature VARCHAR(10) NOT NULL,
                price DECIMAL(5,2) NOT NULL,
                active TINYINT(1) NOT NULL DEFAULT 1
            )
        """)
        cursor.execute("SELECT COUNT(*) AS total FROM bubble_teas")
        if cursor.fetchone()["total"] == 0:
            cursor.executemany(
                "INSERT INTO bubble_teas (name, temperature, price, active) VALUES (%s, %s, %s, %s)",
                [
                    ("Té de Burbuja Clásico",    "hot",  3.99, 1),
                    ("Té de Burbuja de Fresa",   "cold", 4.49, 1),
                    ("Té de Burbuja de Mango",   "cold", 4.99, 1),
                    ("Té de Burbuja de Lichi",   "cold", 5.49, 1),
                    ("Té de Burbuja de Chocolate","hot", 5.99, 0),
                ],
            )
        conn.commit()
    print("Tabla creada e datos insertados correctamente.")
