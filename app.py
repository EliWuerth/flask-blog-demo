import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "mysecretkey"


# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

# Function to retrieve a post from the database
def get_post(post_id):
    # get connection to database
    conn = get_db_connection()

    # create a cursor object
    cur = conn.cursor()

    # execute SQL query to select the post with the given id from the posts table and fetch the post from the cursor
    post = cur.execute("SELECT * FROM posts WHERE id=?", (post_id,)).fetchone()

    # close the cursor and connection
    cur.close()
    conn.close()

    # if no post was found, return None
    if post is None:
        abort(404)

    # return the post
    return post

# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    # get connection to database
    conn = get_db_connection()

    # create a cursor object
    cur = conn.cursor()

    # execute SQL query to select all posts from the posts table
    cur.execute("SELECT * FROM posts")

    # fetch all rows from the cursor
    post = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    # render the index.html template with the fetched rows
    return render_template('index.html', posts=post)

# route to create a post
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # get form data
        title = request.form['title']
        content = request.form['content']

        # validate form data
        if not title and not content:
            flash('Title and Content are required!')
            return redirect(url_for('create'))
        elif not content:
            flash('Content is required!')
            return redirect(url_for('create'))
        elif not title:
            flash('Title is required!')
            return redirect(url_for('create'))

        # get connection to database
        conn = get_db_connection()

        # create a cursor object
        cur = conn.cursor()

        # execute SQL query to insert a new post into the posts table
        cur.execute("INSERT INTO posts (title, content) VALUES (?,?)", (title, content))

        # commit the changes to the database
        conn.commit()

        # close the cursor and connection
        cur.close()
        conn.close()

        # redirect to the index page
        return redirect(url_for('index'))

    else:
        # render the create.html template
        return render_template('create.html')
    

# route to delete a post

# route to update a post
@app.route('/<int:id>/edit/', methods=['GET', 'POST'])
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        pass
        # get form data
        title = request.form['title']
        content = request.form['content']

        # validate form data
        if not title and not content:
            flash('Title and Content are required!')
            return redirect(url_for('edit', id=id))
        elif not content:
            flash('Content is required!')
            return redirect(url_for('edit', id=id))
        elif not title:
            flash('Title is required!')
            return redirect(url_for('edit', id=id))

        # get connection to database
        conn = get_db_connection()

        # create a cursor object
        cur = conn.cursor()

        # execute SQL query to update the post with the given id in the posts table
        cur.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, id))
        
    # render the create.html template
    return render_template('edit.html', post=post)
app.run()