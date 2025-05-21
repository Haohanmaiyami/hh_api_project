import sys
import os

# Добавляем абсолютный путь до src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.append(src_path)

from db import get_connection, create_tables

if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)
    conn.close()
    print("Таблицы успешно созданы в базе данных.")


