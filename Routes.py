from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')

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
        idm = id
        idp = id
    if id == 1:
        id = 1
        idp = id
        idm = id
    return render_template('item.html', trash=trash, idp=idp, idm=idm)

@app.route('/search')
def search():
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM Trash")
    trashes = cur.fetchall()
    return render_template('search.html', trashes=trashes)


if __name__ == "__main__":
    app.run(debug=True)
