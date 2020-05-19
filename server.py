from datetime import date, time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=False, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)

    def __repr__(self):
        return f' User( username: {self.username}, password: {self.password} )'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=False, nullable=False)
    date_posted = db.Column(db.String(15), unique=False, nullable=False)
    
    def __repr__(self):
        return f' Post( content : {self.content}, date_posted : {self.date_posted}) '


@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=reversed(posts))


@app.route("/upload", methods=['GET','POST'])
def upload():
    if request.method == "POST":
        users = User.query.all()
        name = request.form['name']
        password = request.form['password']
        notice = request.form['notice']
        for user in users:
            if user.username == name and user.password == password:
                post = Post(content=str(notice), date_posted=str(date.today()))
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('home'))
            
    return render_template('upload.html')
    

if __name__=='__main__':
    app.run(debug=True)
