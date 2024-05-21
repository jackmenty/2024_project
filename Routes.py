from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT bins FROM Trash")
    bins = cur.fetchone()
    color = "#246eff"
    if bins == 1:
        color = "#246eff"
    if bins == 2 or bins == 6:
        color = "#ff495c"
    if bins == 3 or bins == 5 or bins == 7 or bins == 8:
        color = "#f7cb15"
    if bins == 4:
        color = "#3ddc97"
    return render_template('home.html', bins=bins, color=color)

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/help')
def helppage():
    return render_template('help.html')

@app.route('/item/<int:id>')
def item(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Trash WHERE id=?", (id,))
    trash = cur.fetchone()
    idp = id+1
    idm = id-1
    if id == 10:
        id = 10
        idp = id
    if id == 1:
        id = 1
        idm = id
    cur = conn.cursor()
    cur.execute("SELECT bins FROM Trash WHERE id=?", (id,))
    bins = cur.fetchone()
    color = "#246eff"
    print(bins)
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
    return render_template('search.html', trashes=trashes)


if __name__ == "__main__":
    app.run(debug=True)
