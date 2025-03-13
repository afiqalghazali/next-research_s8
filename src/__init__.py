from flask import Flask

app = Flask(__name__)

# Import route agar otomatis terdaftar saat aplikasi dijalankan
from src.router import db, router
from src.model import save, machine
