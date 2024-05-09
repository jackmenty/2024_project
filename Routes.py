from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/item/<int:id>')
def item(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Trash WHERE id=?", (id,))
    trash = cur.fetchone()
    return render_template('item.html', trash=trash)

@app.route('/search')
def search():
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM Trash")
    trashes = cur.fetchall()
    return render_template('search.html', trashes=trashes)


if __name__ == "__main__":
    app.run(debug=True)
