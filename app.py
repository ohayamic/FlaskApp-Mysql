from flask import Flask, render_template, url_for, request, redirect, flash, session, logging
from wtforms import Form, StringField, PasswordField, validators, TextAreaField
from flask_fontawesome import FontAwesome
from functools import wraps
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from data import Articles
# https://www.youtube.com/watch?v=zRwy8gtgJ1A&list=PLillGF-RfqbbbPz6GSEM9hLQObuQjNoj_

# initialise flask
app = Flask(__name__)
fa = FontAwesome(app)

# config MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'akuJul2018#'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)


#Articles = Articles()


# prevent illegal site viewing.
def isLoggedIn(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You are not an authorised user, please log in', 'danger')
            return redirect(url_for('login'))
    return wrap

# route for the index page
@app.route('/')
def index():
    return render_template('index.html')


# route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# route for the about page
@app.route('/technologies')
def technologies():
    return render_template('technologies.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


# initialise the wtf form library
# for the register form
class RegisterForm(Form):
    name = StringField('Name', validators=[
                       validators.input_required(), validators.length(min=3, max=30)])
    email = StringField(
        'Email', validators=[validators.input_required(), validators.length(min=5, max=50)])
    username = StringField(
        'Username', validators=[validators.input_required(), validators.length(min=5, max=20)])
    password = PasswordField('Password', validators=[validators.input_required(
    ), validators.equal_to('confirmPassword', message='password does not match')])
    confirmPassword = PasswordField(
        'Confrim Password', validators=[validators.input_required()])

# using the register form for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # initialise form
    form = RegisterForm(request.form)

    if request.method == 'POST':
        # get values form form
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # initialise cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, username, email, password) values(%s, %s, %s, %s)",
                    (name, username, email, password))

        # commit cursor to DB
        mysql.connection.commit()

        # close cursor
        cur.close()

        # add a flash message
        flash('You are now registered', category='success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


# the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #form = LoginForm(request.form)
    if request.method == 'POST':
        # get user info from formfields
        username = request.form['username']
        formPassword = request.form['password']

        # create a cursor
        cur = mysql.connection.cursor()

        # Get user info from database
        userDetail = cur.execute(
            "SELECT * FROM users WHERE username = %s", [username])

        if userDetail > 0:
            data = cur.fetchone()   # fetch one and only one page from the database
            password = data["password"]

            # compare the encrypted passwords with the password entered
            if sha256_crypt.verify(formPassword, password):
                # get user info and store in web session
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('articles'))
            else:
                error = 'Passwords do not match'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logout', 'success')
    return redirect(url_for('login'))

# Not in use for now


class ArticleForm(Form):
    title = StringField('Title', validators=[
        validators.input_required(), validators.length(min=3, max=200)])
    body = TextAreaField('Article body', validators=[
        validators.input_required()])


@app.route('/add_article', methods=['GET', 'POST'])
@isLoggedIn  # prevents accessing the url from the web
def add_article():
    form = ArticleForm(request.form)

    # check the request method
    if request.method == 'POST':
        title = form.title.data
        body = form.body.data

        # create a cursor
        cur = mysql.connection.cursor()

        # get article information and prepare it for insert
        cur.execute("INSERT INTO articles(title, author, body) values(%s, %s, %s)",
                    (title, session['username'], body))

        # commit to database
        mysql.connection.commit()

        # close the connection
        cur.close()

        # send a flash message and redirect to articles page
        flash('Article just created successfully', 'success')
        return redirect(url_for('articles'))

    return render_template('add_article.html', form=form)

# route for the articles page
@app.route('/articles')
@isLoggedIn  # prevents accessing the url from the web
def articles():
    # create cursor connection to fetch data
    cur = mysql.connection.cursor()

    # fetch data from database
    result = cur.execute("SELECT * FROM articles")

    # create a logic
    if result > 0:
        articles = cur.fetchall()
        return render_template('articles.html', articles=articles)
    else:
        msg = "There is not article stored"
        return render_template('articles.html', msg=msg)

    # close the connection
    cur.close()
    # return render_template('articles.html', articles=Articles)

# route for the single article page
@app.route('/article/<string:id>/')
@isLoggedIn  # prevents accessing the url from the web
def article(id):
    # create cursor to access the database
    cur = mysql.connection.cursor()

    # make query to the database
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    # apply logic to know if result got a value
    if result > 0:
        article = cur.fetchone()

        # pass the article retrieved to be displayed in browser
        return render_template('article.html', article=article)
    else:
        msg = 'No result found for your search'
        return render_template('article.html', msg=msg)
    cur.close()


@app.route('/delete_article/<string:id>/', methods=['GET', 'POST'])
@isLoggedIn  # prevents accessing the url from the web
def delete_article(id):
    # create cursor to access the database
    cur = mysql.connection.cursor()

    # make query to the database
    result = cur.execute("DELETE FROM articles WHERE id = %s", [id])

    mysql.connection.commit()

    cur.close()
    flash('Article deleted', 'success')

    return redirect(url_for('articles'))
   
    


@app.route('/edit_article/<string:id>/', methods=['GET', 'POST'])
@isLoggedIn  # prevents accessing the url from the web
def edit_article(id):

    # create cursor to access the database
    cur = mysql.connection.cursor()

    # make query to the database
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    # fetch the article
    article = cur.fetchone()

    # get the form
    form = ArticleForm(request.form)

    # populate form using data from database
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():

        title = request.form['title']
        body = request.form['body']

        cur = mysql.connection.cursor()

        cur.execute(
            "UPDATE articles SET title=%s, body=%s WHERE id=%s", (title, body, id))
        mysql.connection.commit()

        cur.close()

        flash('You have successfully edited the article', 'success')
        return redirect(url_for('articles'))
    return render_template('edit_article.html', form=form)


if __name__ == "__main__":
    app.secret_key = "secret12345"
    app.run(debug=True)
