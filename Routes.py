from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/') #Route to the homepage
def homepage():
    color = "#246eff" #this variable defines the navigation bar color, this will appear in most pages
    return render_template('home.html', color=color)

@app.route('/about') #Route to the about page
def aboutpage():
    color = "#246eff"
    return render_template('about.html', color=color)

@app.route('/help') #Route to the help page
def helppage():
    color = "#246eff"
    return render_template('help.html', color=color)

@app.route('/item/<int:id>') #Route to a page about an item
def item(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Trash WHERE id=?", (id,))  #Selects all information of a row where the ID equals to the page ID
    trash = cur.fetchone()
    idp = id+1
    idm = id-1
    if id == 10: #Limits the user for going past the page beyond the number of items
        id = 10
        idp = id
    if id == 1: #Limits the user for going past the page beyond the number of items
        id = 1
        idm = id
    cur = conn.cursor()
    cur.execute("SELECT bins FROM Trash WHERE id=?", (id,))
    bins = cur.fetchone()
    color = "#246eff"
    if bins == (1,):
        color = "#246eff"
    if bins == (2,) or bins == (6,):
        color = "#ff495c"
    if bins == (3,) or bins == (5,) or bins == (7,) or bins == (8,):
        color = "#f7cb15"
    if bins == (4,):
        color = "#3ddc97"
    return render_template('item.html', trash=trash, idp=idp, idm=idm, color=color)

@app.route('/search')
def search():
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM Trash")
    trashes = cur.fetchall()
    color = "#246eff"
    return render_template('search.html', trashes=trashes, color=color)


if __name__ == "__main__":
    app.run(debug=True)
