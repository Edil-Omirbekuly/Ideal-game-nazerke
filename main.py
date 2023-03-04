import requests
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.app_context().push()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accountsdb.db"
# initialize the app with the extension
db.init_app(app)


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30))
    realname = db.Column(db.String(20))
    realsurname = db.Column(db.String(20))
    telephone = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)

class newsdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    img_source = db.Column(db.String)
    author = db.column(db.String)
    release_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
        return render_template("index.html")


@app.route('/indexsign')
def index1():
        return render_template("indexsign.html")

@app.route('/inde_2')
def inde_2():
    return render_template('inde_2.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        login = Register.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect("/indexsign")
        try:
            db.session.commit()
        except:
            return redirect("/indexsign")
    return render_template("login.html")



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        uname = request.form['uname']
        passw = request.form['passw']
        rname = request.form["rname"]
        sname = request.form["sname"]
        tel = request.form["tel"]
        email = request.form["email"]
        register = Register(username=uname, password=passw, realname=rname, realsurname=sname, telephone=tel, email=email)
        db.session.add(register)
        db.session.commit()
        return redirect("/login")
    return render_template("registration.html")

@app.route('/user_profile')
def user_profile():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        user = Register(realname=firstname,
                        realsurname=lastname)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/user_profile')
        except:
            return 'Lala'
    user1 = Register.query.order_by().all()
    return render_template('user_profile.html', user=user1)

@app.route('/admin_profile')
def admin_profile():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        user = Register(realname=firstname,
                        realsurname=lastname)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/user_profile')
        except:
            return 'Lala'
    user1 = Register.query.order_by().all()
    return render_template('user_profile.html', user=user1)


@app.route('/news')
def news():
    #newsList = ['133087',' 133084',' 133085', '133083', '133082', '133080', '133081', '133079', '133078', '133077', '133076', '133074']
    url_news = "https://api.worldnewsapi.com/search-news?api-key=52c4c42930be4a55b9970712a9e80916&text=Xbox"
    rnews = requests.get(url_news).json()
    case = {
        "news": rnews["news"]
     }
    return render_template("news.html", cases=case)

@app.route('/mynews', methods=['GET', 'POST'])
def mynews():
    if request.method == 'POST':
        addnews_title = request.form['addTitle']
        addnews_content = request.form['addContent']
        addnews_img_source = request.form['addSource']
        all_news = newsdb(title=addnews_title,
                          content=addnews_content,
                          img_source=addnews_img_source)

        try:
            db.session.add(all_news)
            db.session.commit()
            return redirect('/mynews')
        except:
            return 'Can not add the title.'
    else:
        news = newsdb.query.order_by(newsdb.release_date).all()
        return render_template('mynews.html', allnews=news)

@app.route('/addnews', methods=['GET', 'POST'])
def addnews():
    if request.method == 'POST':
        addnews_title = request.form['addTitle']
        addnews_content = request.form['addContent']
        addnews_img_source = request.form['addSource']
        addnews_author = request.form['addAuthor']

        all_news = newsdb(title=addnews_title,
                          content=addnews_content,
                          img_source=addnews_img_source,
                          author=addnews_author)
        try:
            db.session.add(all_news)
            db.session.commit()
            return redirect('/addnews')
        except:
            return 'Can not add the title.'
    else:
        news = newsdb.query.order_by(newsdb.release_date).all()
        return render_template('addnews.html', allnews=news)

@app.route('/delete/<int:id>')
def delete(id):
    all_to_delete = newsdb.query.get_or_404(id)
    try:
        db.session.delete(all_to_delete)
        db.session.commit()
        return redirect('/mynews')
    except:
        return "OOPs!"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    update = newsdb.query.get_or_404(id)
    if request.method == 'POST':
        update.title = request.form['addTitle']
        update.content = request.form['addContent']
        update.img_source = request.form['addSource']

        try:
            db.session.commit()
            return redirect('/mynews')
        except:
            return 'There was issue at updating'
    else:
        return render_template("update.html", news=update)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
