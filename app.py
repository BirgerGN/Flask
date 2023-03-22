from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

import bcrypt


app = Flask(__name__)

app.secret_key = 'uwu'


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/enternew')
def new_login():
    return render_template('lag.html')

@app.route('/start')
def start():
    if session:
        return render_template('index.html')
    return render_template('login.html')

@app.route('/rid')
def rid():
    return render_template('D_slett.html')

@app.route('/upd')
def upd():
    return render_template('Oppdater.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("start")

@app.route('/logon')
def logon():
    if session:
        return redirect('start')
    return render_template('login.html')

@app.route('/addrec', methods=['POST','GET'])
def addrec():
    msg = ""
    username=request.form['username']
    pwd=request.form['pwd']

    hashed_password =  bcrypt.hashpw(bytes(pwd, "UTF-8"), bcrypt.gensalt())

    print(username)
    print(pwd)
    with sql.connect("database.db") as con:

        cur = con.cursor()
        cur.execute("INSERT INTO login (username, pwd) VALUES (?,?)",(username, hashed_password))
        con.commit()

        msg = "Record sucessfully added"
        return render_template("result.html", msg=msg)


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        pwd=request.form['pwd']

        with sql.connect("database.db") as con:
            cur = con.cursor()
    
            try: 
                cur.execute(f"SELECT * FROM login WHERE username = '{username}'")
                records = cur.fetchall()
                print(records)

                if len(records) > 0 and bcrypt.checkpw(bytes(pwd, "UTF-8"), records[0][1]):
                    session['username'] = request.form['username']
                    return redirect("start") 
                else:
                    return redirect("logon") 
            except Exception as e: print(e)


@app.route('/slett', methods=['POST','GET'])
def slett():
    username=request.form['username']
    pwd=request.form['pwd']
    

    with sql.connect("database.db") as con:
        cur = con.cursor()

        cur.execute(f"SELECT * FROM login WHERE username='{username}'")
        records = cur.fetchall()

        if len(records) > 0 and bcrypt.checkpw(bytes(pwd, "UTF-8"), records[0][1]):
            cur.execute("DELETE FROM login WHERE username=? ",(username))
            con.commit()
            return render_template("result.html", msg=f"Deltetd {username}")
        else:
            return render_template("result.html", msg="Failed to delete")


@app.route('/oppda', methods=['POST','GET'])
def oppda():
    from_username=request.form['from_username']
    from_pwd=request.form['from_pwd']
    to_username=request.form['to_username']
    to_pwd=request.form['to_pwd']

    with sql.connect("database.db") as con:
        cur = con.cursor()

        cur.execute(f"SELECT * FROM login WHERE username='{from_username}'")
        records = cur.fetchall()

        if len(records) > 0 and bcrypt.checkpw(bytes(from_pwd, "UTF-8"), records[0][1]):
            try:


                cur.execute("UPDATE login SET username=?, pwd=? WHERE username=?",(to_username,  bcrypt.hashpw(bytes(to_pwd, "UTF-8"), bcrypt.gensalt()), from_username ))
                con.commit()
                return render_template("result.html", msg=f"Updated {to_username}")
            except:
                return render_template("result.html", msg="Somthing went wrong")
        else:
            return render_template("result.html", msg="Failed to update")

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from login")
    rows = cur.fetchall()


    return render_template('list.html',rows=rows)

if __name__ == "__main__":
    app.run(debug=True)


