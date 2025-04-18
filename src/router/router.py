from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    jsonify,
)
from .db import get_db  # Import koneksi database dari db.py
from werkzeug.utils import secure_filename
from src.model.save import pushDB, pushImg, pushPassword
from src.model.machine import detek, predFace
import os
import glob
import base64
from flask_login import UserMixin, login_user, logout_user, current_user

router = Blueprint("router", __name__)
conn, cursor = get_db()


class User(UserMixin):
    def __init__(self, id, nama, role):
        self.id = id
        self.nama = nama
        self.role = role


@router.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    cursor.execute("SELECT * FROM user WHERE id = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        if user_data["id"] == username and user_data["password"] == password:
            user = User(user_data["id"], user_data["nama"], user_data["role"])
            login_user(user)

            if user.role == "admin":
                return redirect(url_for("router.home"))
            return redirect(url_for("router.user_home", id=user.id))
        else:
            error = "Password salah"
    else:
        error = "Akun tidak terdaftar"

    return render_template("index.html", error=error)


@router.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("router.index"))


@router.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@router.route("/<string:id>/home", methods=["GET", "POST"])
def user_home(id):
    if request.method == "POST":
        newPassword = request.form.get("newPassword")
        res = pushPassword(id, newPassword)
        if res is not True:
            return jsonify({"error": "Gagal menyimpan user", "message": res}), 500

    # GET atau setelah POST sukses, ambil ulang data user
    cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
    user_data = cursor.fetchone()
    return render_template("user_home.html", user=user_data)
    


@router.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        identityNumber = request.form.get("identityNumber")
        name = request.form.get("name")
        unit = request.form.get("unit")

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


@router.route("/detect", methods=["GET", "POST"])
def detect():
    user_data = ''
    if request.method == "GET":
        return render_template("detect.html")  # Halaman awal tanpa data

@router.route("/detect/image", methods=["POST"])
def pred():
    # Proses POST (saat gambar dikirim)
    if "images" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["images"]
    getId = detek(image)  # Fungsi deteksi wajah

    if not getId:
        return jsonify({"error": "No face detected or ID not found"}), 404

    cursor.execute("SELECT * FROM user WHERE id = %s", (getId,))
    user_data = cursor.fetchone()

    if user_data:
        return jsonify(user_data)  # Kirim data JSON
    else:
        user = ""
        return render_template("detect.html", user=user)



@router.route("/database", methods=["GET"])
def database():
    data = cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()  # Ambil hasil query
    return render_template("database.html", users=data)


@router.route("/user/<string:user_id>/images", methods=["GET"])
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


@router.route("/<id>/delete")
def delete(id):
    # Hapus gambar terkait user
    imgFolder = current_app.config["UPLOAD_FOLDER"]
    image_paths = glob.glob(os.path.join(imgFolder, f"{id}_*.jpg"))

    for image_path in image_paths:
        os.remove(image_path)  # Hapus file gambar

    # Hapus user dari database
    cursor.execute("DELETE FROM user WHERE id = %s", (id,))
    conn.commit()

    return redirect(url_for("router.database"))
