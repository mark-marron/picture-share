from flask import Flask, render_template, url_for, redirect, session, request
from flask_session import Session
from database import get_db, close_db
from forms import RegistrationForm, LoginForm, PostForm, SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "static/assets"
Session(app)


@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    
    db = get_db()
    images = get_images()
    return render_template("index.html", images=images)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        user = db.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchone()

        if user is None:
            form.username.errors.append("Unknown Username")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("Incorrect Password")
        else:
            session.clear()
            session["username"] = username
            session["user_id"] = user["user_id"]
            print(session["username"], session["user_id"])
            return redirect(url_for("index"))

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db = get_db()
        username = form.username.data
        password = form.password1.data
        user = db.execute("""SELECT * FROM users WHERE username=?""", (username,)).fetchone()
        
        if user is not None:
            form.username.errors.append("Username is already in use")
        else:
            db.execute("""INSERT into users (username, password)
                          VALUES (?, ?)""",(username, generate_password_hash(password)))
            db.commit()
            session["username"] = username
            session["user_id"] = user["user_id"]
            return redirect(url_for("index"))

    return render_template("register.html", form=form)

@app.route("/post", methods=["GET", "POST"])
def post():
    if "username" not in session:
        return redirect(url_for("login"))

    form = PostForm()
    if form.validate_on_submit() and request.method == "POST":
        if 'image' not in request.files:
            return render_template("post.html", form=form)
        file = request.files["image"]
        if file:
            caption = form.caption.data

            filename = secure_filename(file.filename)
            timestamp = str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
            new_filename = str(uuid.uuid4()) + timestamp + ".jpg"

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            os.rename(os.path.join(app.config["UPLOAD_FOLDER"], filename), os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
            db = get_db()
            db.execute("""INSERT INTO posts (image_id, user_id, timestamp, caption)
                          VALUES (?, ?, ?, ?)""",(new_filename, session["user_id"], timestamp, caption))
            db.commit()
        
    return render_template("post.html", form=form)

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    print(user_id)
    images = get_images(user_id)
    return render_template("profile.html", images = images)

@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    users = None

    if form.validate_on_submit():
        username = form.username.data
        db = get_db()
        users = db.execute("""SELECT username, user_id 
                              FROM users 
                              WHERE username LIKE ?""", (f'{username}%',)).fetchall()

    return render_template("search.html", form=form, users=users)

@app.route("/user/<user_id>")
def user(user_id):
    images = get_images(user_id)
    return render_template("user.html", images = images)

# functions

def get_images(*user_id):
    db = get_db()
    print(user_id)
    print(type(user_id))
    if user_id:
        return db.execute("""SELECT p.image_id, p.caption, u.username 
                             FROM posts p, users u 
                             WHERE p.user_id = u.user_id
                             AND p.user_id = ?""", (user_id[0],)).fetchall()
    else:
        return db.execute("""SELECT p.image_id, p.caption, u.username 
                             FROM posts p, users u 
                             WHERE p.user_id = u.user_id""").fetchall()

if __name__ == "__main__":
    app.run(debug=True)