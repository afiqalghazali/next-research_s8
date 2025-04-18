from flask import Flask
import mysql.connector

# Buat koneksi global saat aplikasi start
conn = None
cursor = None


def init_db():
    global conn, cursor
    conn = mysql.connector.connect(
        host="localhost",
        database="unimed",
        user="root",
        password="",
        port="3306",  # Hapus port ini kalo mysql anda menggunakan port 3306
    )
    cursor = conn.cursor(dictionary=True)


# Fungsi untuk mendapatkan koneksi yang sudah dibuat
def get_db():
    global conn, cursor
    if conn is None or not conn.is_connected():
        init_db()
    return conn, cursor


# Panggil init_db() saat file ini diimpor
init_db()
