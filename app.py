import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True



# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn


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
    rows = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    # render the index.html template with the fetched rows
    return render_template('index.html', posts=rows)

# route to create a post
app.run()