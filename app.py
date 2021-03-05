import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

mongo = PyMongo(app)


@app.route("/")
@app.route("/homepage", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        mongo.db.users.insert_one({"username": request.form.get("username")})
    return render_template("index-test.html")


@app.route("/profile/<username>/upload/", methods=["GET", "POST"])
def upload_image(username):

    if request.method == 'POST':
        for item in request.files.getlist("image_file"):
            filename = secure_filename(item.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id_image = (username + '/' + filename)
            public_id_video = ("vidoes/" + username + "/" + filename)
            cloudinary.uploader.unsigned_upload(
                item, "puppy_image", cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_image)
            cloudinary.uploader.unsigned_upload(
                user_video, "puppy_image",
                cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_image,
                resource_type="video")
            image_url = (
                "https://res.cloudinary.com/puppyplaymates/image/upload/doubleshamrocks/"
                + public_id_image + file_extension)
            video_url = (
                "https://res.cloudinary.com/puppyplaymates/image/upload/doubleshamrocks/"
                + public_id_video + file_extension)

            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$addToSet": {"user_images": image_url}})

            return redirect(url_for('profile_image', username=username))
            return render_template("profile_image.html", username=username)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
