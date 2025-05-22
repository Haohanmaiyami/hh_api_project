import os
import sys

from db import create_tables, get_connection

# Добавляем абсолютный путь до src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.append(src_path)


if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    conn.close()
    print("Таблицы успешно созданы в базе данных.")
