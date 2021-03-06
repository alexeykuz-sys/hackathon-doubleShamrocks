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

    return render_template("home.html")


@app.route("/upload_video", methods=["GET", "POST"])
def upload_video():
    username = "testing"
    user = mongo.db.users.find_one({"username": username})
    if request.method == 'POST':
        for user_video in request.files.getlist("user_videos"):
            print(user_video)
            filename = secure_filename(user_video.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id_video = ("vidoes/" + username + "/" + filename)
            cloudinary.uploader.unsigned_upload(
                user_video, "puppy_image",
                cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_video,
                resource_type="video")
            video_url = (
                "https://res.cloudinary.com/puppyplaymates/video/upload/doubleshamrocks/"
                + public_id_video + file_extension)

            mongo.db.users.update(
                {"username": username},
                {"$addToSet": {"user_videos": {
                    "video_url": video_url,
                    "video_title": request.form.get('video_title'),
                    "video_description": request.form.get('video_description')
                }}})

        return redirect(url_for('upload_video'))
    return render_template("upload_video.html", user=user)


@app.route("/upload_jokes", methods=["GET", "POST"])
def upload_jokes():
    username = "testing"
    user = mongo.db.users.find_one({"username": username})

    if request.method == 'POST':
        mongo.db.users.update_one(
            {"username": username},
            {"$addToSet": {"user_jokes": request.form.get('user_jokes')}})

        return redirect(url_for('upload_jokes'))
    return render_template("upload_jokes.html", user=user)
 

@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():

    username = "testing"
    user = mongo.db.users.find_one({"username": username})

    if request.method == 'POST':
        for item in request.files.getlist("user_image"):
            filename = secure_filename(item.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id_image = (username + '/' + filename)
            cloudinary.uploader.unsigned_upload(
                item, "puppy_image", cloud_name='puppyplaymates',
                folder='/doubleshamrocks/', public_id=public_id_image)
            image_url = (
                "https://res.cloudinary.com/puppyplaymates/image/upload/doubleshamrocks/"
                + public_id_image + file_extension)

            mongo.db.users.update(
                {"username": username},
                {"$addToSet": {"user_image": {
                    "image_url": image_url,
                    "image_title": request.form.get('image_title'),
                    "image_description": request.form.get('image_description')
                }}})

        return redirect(url_for('upload_image'))
    return render_template("upload_image.html", user=user)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
