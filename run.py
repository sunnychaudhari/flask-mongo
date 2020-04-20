from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from functools import wraps
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'ecom_db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecom_db'

mongo = PyMongo(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

@app.route('/')
def index():
    products = mongo.db.products
    all_products = products.find()
    login = True
    if not session.get ('username'):
        login = False
    return render_template('index.html', all_products=all_products, login=login)

@app.route("/cart/")
@login_required
def cart():
    return render_template ('cart.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8').decode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index'))

        return 'Invalid username/password combination'

    return render_template ('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['name'],'email' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
