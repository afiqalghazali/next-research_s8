from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.router import get_db
from src.router.router import router, User
from flask_mysqldb import MySQL
from flask_login import LoginManager

server = Flask(__name__)

# koneksi database.
conn, cursor = get_db()

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "router.login"


@login_manager.user_loader
def load_user(id):
    cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
    user_data = cursor.fetchone()

    if user_data:
        return User(user_data["id"], user_data["nama"], user_data["role"])
    return None


@server.route("/")
def index():
    return render_template("index.html")


UPLOAD_FOLDER = "static/uploads"
server.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
server.secret_key = "supersecretkey"

# Register Blueprint
server.register_blueprint(router)


if __name__ == "__main__":
    server.run(debug=True)
