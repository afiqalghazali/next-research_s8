from flask import Flask, current_app
from werkzeug.utils import secure_filename
from .machine import regisWajah
import os
import mysql.connector
from src.router.db import get_db

conn, cursor = get_db()

def pushDB(id, nama, unitKerja):
    # Simpan data user ke MySQL
    role = "user"
    try:
        cursor.execute(
            "INSERT INTO user (id, nama, unitKerja, role, password) VALUES (%s, %s, %s, %s, %s)",
            (id, nama, unitKerja, role, id),
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    
def pushPassword(id, newPw):
    try:
        cursor.execute(
            "UPDATE user SET password = %s WHERE id = %s",
            (newPw, id),
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)

def pushImg(user_id, files):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    for i, file in enumerate(files):
        if file:
            filename = secure_filename(f"{user_id}_{i}.jpg")
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
    
    regis = regisWajah(user_id)
    if regis is not True:
        return EOFError

