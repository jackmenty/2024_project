from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
DEFAULT = "#246eff"
RECYCLE = "#f7cb15"
TRASH = "#ff495c"
COMPOST = "#3ddc97"
HIDDEN = "hidden"
PAGINATION = 10


@app.errorhandler(404)
def page_not_found(e):
    color = DEFAULT
    return render_template('404.html', color=color)


@app.route('/')
def homepage():
    color = DEFAULT
    return render_template('home.html', color=color)


@app.route('/about')
def aboutpage():
    color = DEFAULT
    return render_template('about.html', color=color)


@app.route('/pass', methods=["GET", "POST"])
def passwordpage():
    color = DEFAULT
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT pass FROM Password")
    correct_password = cur.fetchone()
    if request.method == "POST":
        password = request.form.get('pass')
        if password == correct_password[0]:
            return redirect(url_for('pendingpage'))
        elif password != correct_password[0]:
            return redirect(url_for('homepage'))
    return render_template('password.html', color=color)


@app.route('/pending', methods=["GET", "POST"])
def pendingpage():
    color = DEFAULT
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pending")
    trashes = cur.fetchall()
    return render_template('pending.html', color=color, trashes=trashes)


@app.route('/penditem/<int:id>', methods=["GET", "POST"])
def pendingitempage(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pending WHERE id=?", (id,))
    trash = cur.fetchone()
    cur.execute("SELECT id FROM Pending ORDER BY ID DESC")
    max_limit = cur.fetchone()
    next_button = id+1
    previous_button = id-1
    next_by_10_button = id+10
    previous_by_10_button = id-10
    hide_previous_by_10_button = None
    hide_next_by_10_button = None
    hide_next_button = None
    hide_previous_button = None
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
    # Checks if there is any item in pending table
    if max_limit[0] is None:
        return redirect(url_for('homepage'))
    # Checks if user exceeds past the max limit of the pending table
    if id > max_limit[0]:
        return redirect(url_for('homepage'))
    # Limits the user for going past the max limit
    if id == max_limit[0] or id >= max_limit[0]:
        id = max_limit[0]
        next_button = id
        next_by_10_button = id
        hide_next_button = HIDDEN
    # Checks if user goes below the minimum database limit
    if id <= 0:
        return redirect(url_for('homepage'))
    # Limits the user for going below the minimum limit
    if id == 1:
        hide_previous_button = HIDDEN
    # Checks for the 'go previous by 10 button'
    if id <= PAGINATION:
        hide_previous_by_10_button = HIDDEN
    # Checks for the 'go forward  by 10 button'
    if id+9 >= max_limit[0]:
        hide_next_by_10_button = HIDDEN
    cur = conn.cursor()
    cur.execute("SELECT bins FROM Pending WHERE id=?", (id,))
    bins = cur.fetchone()
    color = DEFAULT
    # Below conditions checks number for unique colors
    if bins == (1,):
        color = DEFAULT
    if bins == (2,) or bins == (6,):
        color = TRASH
    if bins == (3,) or bins == (5,) or bins == (7,) or bins == (8,):
        color = RECYCLE
    if bins == (4,):
        color = COMPOST
    return render_template('pendingitem.html', trash=trash, idp=next_button,
                           idm=previous_button, idp10=next_by_10_button,
                           idm10=previous_by_10_button,
                           hideprev=hide_previous_button,
                           hideforw=hide_next_button,
                           hideprevall=hide_previous_by_10_button,
                           hideforwall=hide_next_by_10_button, color=color)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/help', methods=["GET", "POST"])
def helppage():
    color = DEFAULT
    hidden = HIDDEN
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        bins = request.form.get('bins')
        rrr = request.form.get('rrr')
        # image = request.form.get('image')
        file = request.files['image']
        if 'image' not in request.files:
            print("No file was attached")
        # sends image into the image folder
        if file and allowed_file(file.filename):
            print("got file ok")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("File path is " + os.path.join(app.config['UPLOAD_FOLDER'],
                                                 filename))
        cur.execute("""INSERT INTO Pending (name, description, instructions,
                    bins, rrr, image) VALUES (?,?,?,?,?,?)""",
                    (name, description, instructions, bins, rrr, filename))
        conn.commit()
        conn.close()
        hidden = None
    return render_template('help.html', color=color, hidden=hidden)


@app.route('/item/<int:id>')
def item(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Trash WHERE id=?", (id,))
    trash = cur.fetchone()
    cur.execute("""SELECT * FROM RRR WHERE id =
                (SELECT rrr FROM Trash WHERE id=?)""", (id,))
    rrr = cur.fetchone()
    cur.execute("SELECT id FROM Trash ORDER BY ID DESC")
    max_limit = cur.fetchone()
    next_button = id+1
    previous_button = id-1
    next_by_10_button = id+10
    previous_by_10_button = id-10
    hide_previous_by_10_button = None
    hide_next_by_10_button = None
    hide_next_button = None
    hide_previous_button = None
    # Checks if user exceeds past the max limit of the trash table
    if id > max_limit[0]:
        return redirect(url_for('homepage'))
    # Limits the user for going past the max limit
    if id == max_limit[0] or id >= max_limit[0]:
        id = max_limit[0]
        next_button = id
        next_by_10_button = id
        hide_next_button = HIDDEN
    # Checks if user goes below the minimum database limit
    if id <= 0:
        return redirect(url_for('homepage'))
    # Limits the user for going below the minimum limit
    if id == 1:
        hide_previous_button = HIDDEN
    # Checks for the 'go previous by 10 button'
    if id <= 10:
        hide_previous_by_10_button = HIDDEN
    # Checks for the 'go forward  by 10 button'
    if id+9 >= max_limit[0]:
        hide_next_by_10_button = HIDDEN
    cur = conn.cursor()
    cur.execute("SELECT bins FROM Trash WHERE id=?", (id,))
    bins = cur.fetchone()
    color = DEFAULT
    # Below conditions checks number for unique colors
    if bins == (1,):
        color = DEFAULT
    if bins == (2,) or bins == (6,):
        color = TRASH
    if bins == (3,) or bins == (5,) or bins == (7,) or bins == (8,):
        color = RECYCLE
    if bins == (4,):
        color = COMPOST
    return render_template('item.html', trash=trash, rrr=rrr, idp=next_button,
                           idm=previous_button, idp10=next_by_10_button,
                           idm10=previous_by_10_button,
                           hideprev=hide_previous_button,
                           hideforw=hide_next_button,
                           hideprevall=hide_previous_by_10_button,
                           hideforwall=hide_next_by_10_button, color=color)


@app.route('/search/<int:id>')
def search(id):
    conn = sqlite3.connect("Webdatabase.db")
    cur = conn.cursor()
    # Takes chunks of the table for pagination
    cur.execute("""SELECT id, name, image FROM Trash WHERE id <= ? * 10
                AND id > 10 * (?-1)""", (id, id))
    trashes = cur.fetchall()
    color = DEFAULT
    cur.execute("SELECT id FROM Trash ORDER BY ID DESC")
    max_limit = cur.fetchone()
    hide_next_button = None
    hide_previous_button = None
    next_button = id+1
    previous_button = id-1
    # Checks if user exceeds past the max limit
    if id >= (max_limit[0]/PAGINATION) + 1:
        return redirect(url_for('homepage'))
    # Limits the user from exceeding past the max limit
    if id > (max_limit[0]/PAGINATION):
        id = max_limit[0]
        next_button = id
        hide_next_button = HIDDEN
    # Checks if user goes below the minimum limit
    if id <= 0:
        return redirect(url_for('homepage'))
    # Limits the user from going below the minimum limit
    if id == 1:
        hide_previous_button = HIDDEN
    return render_template('search.html', trashes=trashes, color=color,
                           idp=next_button, idm=previous_button,
                           hideprev=hide_previous_button,
                           hideforw=hide_next_button)


@app.route('/search', methods=['GET', 'POST'])
def searched():
    hide_next_button = HIDDEN
    hide_previous_button = HIDDEN
    if request.method == 'POST':
        conn = sqlite3.connect("Webdatabase.db")
        cur = conn.cursor()
        search = f"%{request.form.get('searchterm')}%"
        color = DEFAULT
        cur.execute("SELECT id, name, image FROM Trash WHERE name LIKE ?",
                    (search, ))
        trashes = cur.fetchall()
        return render_template('search.html', trashes=trashes, color=color,
                               hideprev=hide_previous_button,
                               hideforw=hide_next_button)
    else:
        return render_template('search.html', trashes=trashes, color=color,
                               hideprev=hide_previous_button,
                               hideforw=hide_next_button)


if __name__ == "__main__":
    app.run(debug=True)
