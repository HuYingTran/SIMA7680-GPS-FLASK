import sqlite3
import pytz
from datetime import datetime

def setup_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS table_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        x TEXT NOT NULL,
        y TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        phone TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def write_data(data_t, x_t,y_t,timestamp_t, phone_t):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Chỉnh sửa thời gian theo múi giờ GMT+7 (Việt Nam)
    # vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    # current_time = datetime.now(vietnam_tz).strftime('%Y-%m-%d %H:%M:%S')

    query = f'INSERT INTO "table_data" (data, x, y, timestamp, phone) VALUES (?, ?, ?, ?, ?)'
    cursor.execute(query, (data_t, x_t, y_t, timestamp_t, phone_t))

    conn.commit()
    conn.close()


def get_data_by_time(start_time, end_time):
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Câu lệnh SQL để lấy dữ liệu trong khoảng thời gian
    query = '''
    SELECT * FROM table_data
    WHERE timestamp BETWEEN ? AND ?
    '''

    # Thực thi câu lệnh SQL
    cursor.execute(query, (start_time, end_time))

    # Lấy tất cả các kết quả
    rows = cursor.fetchall()

    # Đóng kết nối
    conn.close()

    return rows


def delete_all_data():
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Xóa tất cả dữ liệu trong bảng nhưng giữ lại cấu trúc
    cursor.execute("DELETE FROM table_data;")
    
    # Commit thay đổi và đóng kết nối
    conn.commit()
    conn.close()

def delete_data_id(ids):
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM table_data WHERE id IN ({','.join('?' for _ in ids)})", ids)

    conn.commit()
    # Đóng kết nối
    conn.close()

def get_all_data():
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Truy vấn dữ liệu từ bảng
    cursor.execute("SELECT * FROM table_data")
    rows = cursor.fetchall()

    # Đóng kết nối
    conn.close()
    return rows