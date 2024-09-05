from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/')  # Route to the homepage
def homepage():
    # variable defines navbar color, repeats on most fucntions
    color = "#246eff"
    return render_template('home.html', color=color)


@app.route('/about')  # Route to the about page
def aboutpage():
    color = "#246eff"
    return render_template('about.html', color=color)


@app.route('/pass', methods=["GET", "POST"])  # Route to the password page
def passwordpage():
    color = "#246eff"
    if request.method == "POST":
        password = request.form.get('pass')
        if 'garboday' not in password:
            return redirect("http://127.0.0.1:5000")
        if 'garboday' == password:
            return redirect("http://127.0.0.1:5000/pending")
    return render_template('password.html', color=color)


@app.route('/pending', methods=["GET", "POST"])  # Route to the pending page
def pendingpage():
    color = "#246eff"
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pending")
    trashes = cur.fetchall()
    if request.method == "POST":
        if "go" in request.form:
            pass
    return render_template('pending.html', color=color, trashes=trashes)


@app.route('/penditem/<int:id>', methods=["GET", "POST"])  # Route to the pending page
def pendingitempage(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    # Selects all info of a row where the ID equals to the page ID
    cur.execute("SELECT * FROM Pending WHERE id=?", (id,))
    trash = cur.fetchone()
    cur.execute("SELECT id FROM Pending ORDER BY ID DESC")
    limitbig = cur.fetchone()
    idp = id+1
    idm = id-1
    idp10 = id+10
    idm10 = id-10
    hideprevall = " "
    hideforwall = " "
    hideforw = " "
    hideprev = " "
    print(request.method)
    if request.method == "POST":
        if "add" in request.form:
            cur.execute("""INSERT INTO Trash (name, description, instructions,
                    bins, rrr, image)VALUES
                    ((SELECT name FROM Pending WHERE id=?),
                    (SELECT description FROM Pending WHERE id=?),
                    (SELECT instructions FROM Pending WHERE id=?),
                    (SELECT bins FROM Pending WHERE id=?),
                    (SELECT rrr FROM Pending WHERE id=?),
                    (SELECT image FROM Pending WHERE id=?))""", (id, id, id,
                                                                 id, id, id,))
            cur.execute("""DELETE FROM Pending WHERE id=?""", (id,))
            conn.commit()
            return redirect("http://127.0.0.1:5000/pending")
        if "delete" in request.form:
            cur.execute("""DELETE FROM Pending WHERE id=?""", (id,))
            conn.commit()
            return redirect("http://127.0.0.1:5000")
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
    cur.execute("SELECT bins FROM Pending WHERE id=?", (id,))
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
    return render_template('pendingitem.html', trash=trash, idp=idp, idm=idm,
                           idp10=idp10, idm10=idm10, hideprev=hideprev,
                           hideforw=hideforw, hideprevall=hideprevall,
                           hideforwall=hideforwall, color=color)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',
                                               1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/help', methods=["GET", "POST"])  # Route to the help page
def helppage():
    color = "#246eff"
    hidden = "hidden"
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    # in other words, someone clicked submit, 'POSTing' info
    # back to the server
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        bins = request.form.get('bins')
        rrr = request.form.get('rrr')
        # image = request.form.get('image')
        file = request.files['image']
        print("start")
        if 'image' not in request.files:
            print("No file was attached")
        if file and allowed_file(file.filename):
            print("got file ok")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("File path is " + os.path.join(app.config['UPLOAD_FOLDER'],
                                                 filename))
        # Stores the inputted info into the database
        cur.execute("""INSERT INTO Pending (name, description, instructions,
                    bins, rrr, image) VALUES (?,?,?,?,?,?)""",
                    (name, description, instructions, bins, rrr, filename))
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
                           hideforw=hideforw)


@app.route('/search', methods=['GET', 'POST'])  # Route to search page
def searched():
    hideforw = "hidden"
    hideprev = "hidden"
    # in other words, someone clicked submit, 'POSTing' info
    # back to the server
    if request.method == 'POST':
        conn = sqlite3.connect("Webdatabase.db")
        cur = conn.cursor()
        search = f"%{request.form.get('searchterm')}%"
        color = "#246eff"
        # here is where you would do a query on your table for the search term
        # provided, have a look at using LIKE and % in SQLite - something like
        cur.execute("SELECT id, name, image FROM Trash WHERE name LIKE ?",
                    (search, ))
        trashes = cur.fetchall()
        return render_template('search.html', trashes=trashes, color=color,
                               hideprev=hideprev, hideforw=hideforw)
    else:
        return render_template('search.html', trashes=trashes, color=color,
                               hideprev=hideprev, hideforw=hideforw)


if __name__ == "__main__":
    app.run(debug=True)
