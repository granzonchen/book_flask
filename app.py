# coding=utf-8
from __future__ import print_function
from flask import Flask, request, render_template, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/bookinfo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# UPLOAD_FOLDER = 'upload'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Book(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    publish = db.Column(db.String(50))
    ISBN = db.Column(db.String(50))
    photo = db.Column(db.String(200))

    def __init__(self, name, author, publish, ISBN, photo):
        self.name = name
        self.author = author
        self.publish = publish
        self.ISBN = ISBN
        self.photo = photo


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def search_result():
    if request.method == 'POST':
        name = request.form['name']
        results = Book.query.filter(Book.name.like('%' + name + '%')).all()
        if results:
            msg = "".join(
                [u"已经为您查找 ", u'“', name, u'”', u" 相关的书籍，结果如下："])
            return render_template('result.html', results=results, name=name, msg=msg)
        else:
            msg = "".join([u"很抱歉，没有找到您查找的 ", u'"', name, u'"', u" 相关书籍。"])
            return render_template('result.html', result=results, name=name, msg=msg)
    else:
        return redirect(url_for('index'))


@app.route('/purchase/', methods=['POST', 'GET'])
def purchase():
    if request.method == 'POST':
        newname = request.form['name']
        newauthor = request.form['author']
        newpublish = request.form['publish']
        newisbn = request.form['isbn']
        newphoto = request.files['photo']
        filename = newphoto.filename
        path = basedir + "/static/upload/"
        file_path = path + filename
        newphoto.save(file_path)
        print(file_path)
        file_photo = 'upload/' + filename
        newbook = Book(name=newname, author=newauthor, publish=newpublish, ISBN=newisbn, photo=file_photo)
        db.session.add(newbook)
        db.session.commit()
        return render_template('success.html', name=newname)
    else:
        return render_template('purchase.html')


@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    if request.method == 'POST':
        addname = request.form['name']
        addauthor = request.form['author']
        addpublish = request.form['publish']
        addisbn = request.form['isbn']
        addphoto = request.form['photo']
        addbook = Book(name=addname, author=addauthor, publish=addpublish, ISBN=addisbn, photo=addphoto)
        db.session.add(addbook)
        db.session.commit()
        return render_template('success.html', user=True, name=addname)
    else:
        return render_template('addbook.html')


@app.route('/success')
def success(name=None):
    if name:
        return render_template('success.html')
    else:
        return render_template('index.html')


@app.route('/purchase/orders/<string:user>', methods=['GET'])
@app.route('/purchase/orders', methods=['GET'])
def list_book(user=None):
    if user == 'admin':
        book_list = Book.query.all()
        return render_template('orders.html', book_list=book_list, user=user)
    else:
        book_list = Book.query.all()[:10]
        return render_template('orders.html', book_list=book_list)


@app.route('/audit', methods=['GET'])
def audit():
    user = request.args.get('user')
    print(user)
    if user:
        book_list = Book.query.all()[:10]
        return render_template('audit.html', book_list=book_list)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
