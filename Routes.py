from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('layout.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/search')
def searchpage():
    return render_template('layout.html', 'search.html')


@app.route('/item/<int:id>')
def item(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bins WHERE id=?", (id,))
    pizza = cur.fetchone()
    return render_template('item.html', pizza=pizza)


if __name__ == "__main__":
    app.run(debug=True)
