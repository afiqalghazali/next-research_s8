import os
import glob
import base64
import cv2
import numpy as np
from os import listdir
from PIL import Image
from numpy import asarray, expand_dims
from keras_facenet import FaceNet
from ultralytics import YOLO
from io import BytesIO
from flask import current_app, jsonify

# Load model deteksi wajah dan FaceNet
HaarCascade = cv2.CascadeClassifier('src/model/haarcascade_frontalface_default.xml')
MyFaceNet = FaceNet()

import pickle

def regisWajah(user_id):
    imgFolder = current_app.config["UPLOAD_FOLDER"]
    
    # Path file penyimpanan database
    pkl_path = os.path.join("src/model", "data.pkl")

    # Coba load database lama jika ada
    if os.path.exists(pkl_path):
        with open(pkl_path, "rb") as file:
            try:
                database = pickle.load(file)
            except EOFError:
                database = {}  # Jika file kosong
    else:
        database = {}

    # Cari semua gambar dengan pola "user_id_*.jpg"
    image_paths = sorted(glob.glob(os.path.join(imgFolder, f"{user_id}_*.jpg")))

    if not image_paths:
        return jsonify({"error": "User not found"}), 404

    for image_path in image_paths:
        filename = os.path.basename(image_path)  # Ambil nama file saja
        gbr1 = cv2.imread(image_path)  # Baca gambar

        # Deteksi wajah
        wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)
        if len(wajah) > 0:
            x1, y1, width, height = wajah[0]
        else:
            x1, y1, width, height = 1, 1, 10, 10  # Jika tidak ada wajah

        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        # Konversi ke RGB dan potong wajah
        gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)
        gbr_array = asarray(gbr)
        face = gbr_array[y1:y2, x1:x2]

        # Resize wajah ke 160x160
        face = Image.fromarray(face)
        face = face.resize((160, 160))
        face = asarray(face)

        # Ekstraksi fitur wajah menggunakan FaceNet
        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)

        # Ambil ID unik dari nama file
        file_parts = filename.split('_')  # Contoh: "user_1234_1.jpg" → ['user', '1234', '1', 'jpg']
        
        if len(file_parts) < 3:
            print(f"WARNING: Format filename tidak sesuai -> {filename}")
            continue
        
        file_id = file_parts[1]  # '1234'
        file_num = file_parts[2].split('.')[0]  # '1' (menghapus ekstensi)
        final_key = file_id + '_' + file_num  # Contoh: '1234_1'

        database[final_key] = signature  # Simpan hasil embedding dalam database

    # Simpan kembali database ke file data.pkl
    with open(pkl_path, "wb") as file:
        pickle.dump(database, file)

    print("Database wajah berhasil diperbarui dan disimpan ke data.pkl!")
    return True

def predFace(file):
    myfile = open("src/model/data.pkl", "rb")
    database = pickle.load(myfile)
    myfile.close()
    wajah = HaarCascade.detectMultiScale(file,1.1,4)

    if len(wajah)>0:
        x1, y1, width, height = wajah[0]
    else:
        x1, y1, width, height = 1, 1, 10, 10

    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height


    gbr = cv2.cvtColor(file, cv2.COLOR_BGR2RGB)
    gbr = Image.fromarray(gbr)                  # konversi dari OpenCV ke PIL
    gbr_array = asarray(gbr)

    face = gbr_array[y1:y2, x1:x2]

    face = Image.fromarray(face)
    face = face.resize((160,160))
    face = asarray(face)

    #face = face.astype('float32')
    #mean, std = face.mean(), face.std()
    #face = (face - mean) / std

    face = expand_dims(face, axis=0)
    #signature = MyFaceNet.predict(face)
    signature = MyFaceNet.embeddings(face)

    min_dist=100
    identity=' '
    for key, value in database.items() :
        dist = np.linalg.norm(value-signature)
        if dist < min_dist:
            min_dist = dist
            identity = key
    return identity

def detek(file):
    model = YOLO('src/model/best.pt')  # Load model YOLO
    folder = "static/plat/"  # Folder untuk menyimpan hasil crop

    # ✅ Baca file sebagai numpy array
    file_bytes = np.frombuffer(file.read(), np.uint8)  
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Decode ke format gambar

    if img is None:
        print("❌ Gagal membaca gambar! Cek format file.")
        return None

    # ✅ Simpan gambar sementara agar YOLO bisa membacanya
    temp_path = "temp_image.jpg"
    cv2.imwrite(temp_path, img)

    # ✅ Gunakan path file, bukan numpy array, untuk YOLO
    results = model.predict(temp_path)  
    getId = predFace(img)  # Deteksi wajah

    # Looping hasil deteksi untuk mencari objek 'plat'
    for i, result in enumerate(results):
        for j, (box, cls) in enumerate(zip(result.boxes.xyxy, result.boxes.cls)):
            class_id = int(cls.item())  # Ambil class index
            
            if class_id == 1:  # Ganti 1 dengan index class plat di model YOLO-mu
                x1, y1, x2, y2 = map(int, box)  # Bounding box koordinat
                cropped_img = img[y1:y2, x1:x2]  # Crop gambar

                # Pastikan folder ada sebelum menyimpan file
                if not os.path.exists(folder):
                    os.makedirs(folder)

                # Simpan gambar hasil crop
                cropped_filename = os.path.join(folder, f"{getId}_plat.jpg")
                cv2.imwrite(cropped_filename, cropped_img)

    # ✅ Hapus gambar sementara
    os.remove(temp_path)

    return getId  # Return ID hasil deteksi wajah