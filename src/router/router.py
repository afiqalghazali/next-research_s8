from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from .db import get_db  # Import koneksi database dari db.py
from werkzeug.utils import secure_filename
from src.model.save import pushDB, pushImg
import os
import glob
import base64

router = Blueprint('router', __name__)
conn, cursor = get_db()
@router.route('/register', methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        identityNumber = request.form.get('identityNumber')
        name = request.form.get('name')
        unit = request.form.get('unit')

        res = pushDB(identityNumber, name, unit)
        if res is not True:
            return jsonify({"error": "Gagal menyimpan user", "message": res}), 500
        
        user_id = identityNumber  # Ambil ID user yang baru dimasukkan

        # Cek apakah ada file gambar
        if "images" in request.files:
            files = request.files.getlist("images")
            resImg = pushImg(user_id, files)
        
        return redirect(url_for("router.register"))

    return render_template("register.html")


@router.route('/database', methods=['GET'])
def database():
    data = cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()  # Ambil hasil query
    return render_template('database.html', users=data)


@router.route('/user/<string:user_id>/images', methods=['GET'])
def get_user_images(user_id):
    imgFolder = current_app.config["UPLOAD_FOLDER"]

    # Cari gambar dengan pola "user_id_*.jpg"
    image_paths = sorted(glob.glob(os.path.join(imgFolder, f"{user_id}_*.jpg")))

    if not image_paths:
        return jsonify({"error": "User not found"}), 404

    images_encoded = {}

    # Batasi hanya ambil 5 gambar pertama
    for i, image_path in enumerate(image_paths[:5]):  
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            images_encoded[f"image_{i}"] = encoded  # Pakai format JSON yang sesuai

    return jsonify(images_encoded), 200


@router.route('/<id>/delete')
def delete(id):
    # Hapus gambar terkait user
    imgFolder = current_app.config["UPLOAD_FOLDER"]
    image_paths = glob.glob(os.path.join(imgFolder, f"{id}_*.jpg"))

    for image_path in image_paths:
        os.remove(image_path)  # Hapus file gambar

    # Hapus user dari database
    cursor.execute("DELETE FROM user WHERE id = %s", (id,))
    conn.commit()

    return redirect(url_for('router.database'))

