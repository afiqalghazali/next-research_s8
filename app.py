from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import GridFS
import base64

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.detection_database
users = db.users
fs = GridFS(db, collection='images')


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        identityNumber = request.form.get("identityNumber")
        name = request.form.get("name")
        unit = request.form.get("unit")

        # Insert user record first, then store images with references
        user_doc = {
            "identityNumber": identityNumber,
            "name": name,
            "unit": unit
        }
        user_id = users.insert_one(user_doc).inserted_id

        # Store images in GridFS
        if "images" in request.files:
            files = request.files.getlist("images")
            if len(files) > 0:
                for i, file in enumerate(files):
                    if file:
                        filename = f"{user_id}_{i}.jpg"
                        fs_id = fs.put(file, filename=filename)
                        # Add ref to user document
                        users.update_one(
                            {"_id": user_id},
                            {"$set": {f"image_{i}": fs_id}}
                        )

        return redirect(url_for("register"))
    else:
        return render_template("register.html")


@app.route('/database', methods=['GET'])
def database():
    users_data = users.find()

    return render_template('database.html', users=users_data)


@app.route('/user/<string:user_id>/images', methods=['GET'])
def get_user_images(user_id):
    # Attempt to fetch the user doc
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User   not found"}), 404

    # We expect up to 5 images in fields image_0 .. image_4
    images_encoded = []
    for i in range(5):
        image_key = f"image_{i}"
        if image_key in user:
            fs_id = user[image_key]
            if fs_id:
                # Retrieve from GridFS
                grid_out = fs.get(fs_id)
                # Convert to base64
                file_data = grid_out.read()
                encoded = base64.b64encode(file_data).decode("utf-8")
                images_encoded.append({
                    "base64": encoded
                })

    return jsonify(images_encoded), 200


@app.route('/<id>/delete')
def delete(id):
    # Fetch the user document to get the image IDs
    user = users.find_one({'_id': ObjectId(id)})

    if user:
        # Attempt to delete images from GridFS
        for i in range(5):
            image_key = f"image_{i}"
            if image_key in user:
                fs_id = user[image_key]
                if fs_id:
                    fs.delete(fs_id)  # Delete the image from GridFS

        # Now delete the user document
        users.delete_one({'_id': ObjectId(id)})

    return redirect(url_for('database'))


if __name__ == '__main__':
    app.run(debug=True)
