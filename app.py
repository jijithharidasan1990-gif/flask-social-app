import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysocialsecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social.db'
app.config['UPLOAD_FOLDER'] = "static/uploads"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# ----------------- MODELS -----------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    media = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

# ----------------- ROUTES -----------------
@app.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    if request.method == "POST":
        content = request.form['content']
        file = request.files['media']

        filename = None
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_post = Post(content=content, media=filename, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("create_post.html")

@app.route('/delete/<int:pid>')
@login_required
def delete_post(pid):
    post = Post.query.get(pid)
    if post and post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
