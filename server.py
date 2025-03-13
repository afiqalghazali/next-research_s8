from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.router import get_db
from src.router.router import router
from flask_mysqldb import MySQL

server = Flask(__name__)

#koneksi database.
conn, cursor = get_db()

@server.route('/')
def index():
    return render_template('index.html')

UPLOAD_FOLDER = "static/uploads"
server.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
server.secret_key = "supersecretkey"

# Register Blueprint
server.register_blueprint(router)


if __name__ == '__main__':
    server.run(debug=True)
