import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
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


@app.route("/jokes", methods=["GET", "POST"])
def jokes():
    jokes = list(mongo.db.jokes.find())
    return render_template("jokes.html", jokes=jokes)


@app.route('/joke_like/<joke_id>', methods=["GET", "POST"])
def joke_like(joke_id):
    joke = mongo.db.jokes.find_one_and_update(
        {"_id": ObjectId(joke_id)},
        {'$inc': {'likes': 1}},
        upsert=True
        )
    # jokes.update({'$inc': {'likes': 1}})
    return render_template("jokes.html", jokes=jokes)


@app.route('/joke_dislike/<joke_id>', methods=["GET", "POST"])
def joke_dislike(joke_id):
    print(joke_id)
    jokes = mongo.db.jokes.find_one({"_id": ObjectId(joke_id)})
    jokes.update({'$inc': {'dislikes': 1}})
    # jokes.update({'_id': joke_id}, {'$inc': {'dislikes': 1}})
    return render_template("jokes.html", jokes=jokes)


@app.route("/videos", methods=["GET", "POST"])
def videos():
    return render_template("videos.html")


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


@app.route("/login",  methods=['GET', 'POST'])
def login():
    '''
    The login function calls LoginForm class from the forms.py file,
    It checks if the inputed username and passwords are valid
    and then it adds a user to session.
    '''
    # Check if the user is already logged in
    if 'username' in session:
        flash('You are already logged in!')
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        users = mongo.db.users
        registered_user = users.find_one({'username':
                                          request.form['username']})

        if registered_user:
            # Check if password in the form is same as the password in the DB
            if check_password_hash(registered_user['password'],
                                   request.form['password']):
                # Add user to session if passwords match,
                # redirect user to the homepage after successfull login
                session['username'] = request.form['username']
                flash('You have been successfully logged in!')
                return redirect(url_for('homepage'))
            else:
                # if user entered incorrect password
                flash("Incorrect username or password. Please try again")
                return redirect(url_for('login'))
        else:
            # if user entered incorrect username
            flash("Username does not exist! Please try again")
            return redirect(url_for('login'))
    return render_template('login.html',  form=form)


# Register
@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    CREATE.
    Creates a new account for a new user; it calls the RegisterForm class
     from forms.py file.
    Checks if the username is not already excist in database,
    hashes the entered password and add a new user to session.
    '''
    # checks if user is not already has an account
    if 'username' in session:
        flash('You are already registered!')
        return redirect(url_for('homepage'))

    form = RegisterForm()
    if form.validate_on_submit():
        users = mongo.db.users
        # checks if the username is unique
        registered_user = mongo.db.users.find_one({'username':
                                                   request.form['username']})
        if registered_user:
            flash("Sorry, this username is already taken!")
            return redirect(url_for('register'))
        else:
            # hashes the entered password using werkzeug
            hashed_password = generate_password_hash(request.form['password'])
            new_user = {
                "username": request.form['username'],
                "password": hashed_password,
                "jokes": [],
                "videos": [],
                "images": [],
                "profile_image": "",
            }
            users.insert_one(new_user)
            # add new user to the session
            session["username"] = request.form['username']
            flash('Your account has been successfully created.')
            return redirect(url_for('homepage'))
    return render_template('register.html', form=form)


# Logout
@app.route("/logout")
def logout():
    '''
    Logs user out and redirects to home
    '''
    session.pop("username",  None)
    return redirect(url_for("homepage"))


# Profile
@app.route("/profile/<username>")
def profile(username):
    '''
    Profile page.
    '''
    # prevents guest users from viewing the page
    if 'username' not in session:
        flash('You must be logged in to view that page!')
    username = mongo.db.users.find_one({'username':
                                        session['username']})['username']
    image = mongo.db.users.find_one({'username':
                                     session['username']})['profile_image']
    return render_template('profile.html',
                           image=image,
                           username=username)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
