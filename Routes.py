from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')  # Route to the homepage
def homepage():
    color = "#246eff"  # variable defines navbar color, repeats on most lines
    return render_template('home.html', color=color)


@app.route('/about')  # Route to the about page
def aboutpage():
    color = "#246eff"
    return render_template('about.html', color=color)


@app.route('/help', methods=["GET", "POST"])  # Route to the help page
def helppage():
    color = "#246eff"
    hidden = "hidden"
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        bins = request.form.get('bins')
        rrr = request.form.get('rrr')
        cur.execute("SELECT id FROM Trash ORDER BY ID DESC")
        id = cur.fetchone()
        cur.execute("""INSERT INTO Trash (id, name, description, instructions,
                    bins, rrr) VALUES (?,?,?,?,?,?)""",
                    (id[0]+1, name, description, instructions, bins, rrr))
        conn.commit()
        conn.close()
        hidden = " "
    return render_template('help.html', color=color, hidden=hidden)


@app.route('/item/<int:id>')  # Route to a page about an item
def item(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    # Selects all info of a row where the ID equals to the page ID
    cur.execute("SELECT * FROM Trash WHERE id=?", (id,))
    trash = cur.fetchone()
    cur.execute("SELECT id FROM Trash ORDER BY ID DESC")
    limitbig = cur.fetchone()
    idp = id+1
    idm = id-1
    idp10 = id+10
    idm10 = id-10
    hideprevall = " "
    hideforwall = " "
    hideforw = " "
    hideprev = " "
    # Limits the user for going past page beyond the num of items
    if id == limitbig[0] or id >= limitbig[0]:
        id = limitbig[0]
        idp = id
        idp10 = id
        hideforw = "hidden"
# Limits the user for going past page beyond the num of items
    if id == 1 or id <= 1:
        id = 1
        idm = id
        idm10 = id
        hideprev = "hidden"
    if id <= 10:
        hideprevall = "hidden"
    if id+9 >= limitbig[0]:
        hideforwall = "hidden"
    cur = conn.cursor()
    # Takes the condition number for color
    cur.execute("SELECT bins FROM Trash WHERE id=?", (id,))
    bins = cur.fetchone()
    color = "#246eff"
    # Below conditions checks number for unique colors
    if bins == (1,):
        color = "#246eff"
    if bins == (2,) or bins == (6,):
        color = "#ff495c"
    if bins == (3,) or bins == (5,) or bins == (7,) or bins == (8,):
        color = "#f7cb15"
    if bins == (4,):
        color = "#3ddc97"
    return render_template('item.html', trash=trash, idp=idp, idm=idm,
                           idp10=idp10, idm10=idm10, hideprev=hideprev,
                           hideforw=hideforw, hideprevall=hideprevall,
                           hideforwall=hideforwall, color=color)


@app.route('/search/<int:id>')  # Route to search page
def search(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("""SELECT id, name, image FROM Trash WHERE id <= ? * 10
                AND id > 10 * (?-1)""", (id, id))
    trashes = cur.fetchall()
    color = "#246eff"
    cur.execute("SELECT id FROM Trash ORDER BY ID DESC")
    limitbig = cur.fetchone()
    hideforw = " "
    hideprev = " "
    idp = id+1
    idm = id-1
    # Limits the user going past page beyond the num of items
    if id == 1 or id <= 1:
        id = 1
        idm = id
        hideprev = "hidden"
    if id > round(limitbig[0]/10):
        id = limitbig[0]
        idp = id
        hideforw = "hidden"
    return render_template('search.html', trashes=trashes, color=color,
                           idp=idp, idm=idm, hideprev=hideprev,
                           hideforw=hideforw,)


@app.route('/search', methods=['GET', 'POST'])  # Route to search page
def searched():
    if request.method == 'POST':
        conn = sqlite3.connect("Webdatabase.db")
        cur = conn.cursor()
        # in other words, someone clicked submit, 'POSTing' info
        # back to the server
        search = f"%{request.form.get('searchterm')}%"
        color = "#246eff"
        # here is where you would do a query on your table for the search term
        # provided, have a look at using LIKE and % in SQLite - something like
        cur.execute("SELECT id, name, image FROM Trash WHERE name LIKE ?",
                    (search, ))
        trashes = cur.fetchall()
        return render_template('search.html', trashes=trashes, color=color)
    else:
        return "poop"


if __name__ == "__main__":
    app.run(debug=True)
