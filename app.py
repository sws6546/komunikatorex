from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import dbUsers
import dbMessages
from flask_session import Session

# Zrob sprawdzanie od kogo wiadomosci i do kogo wariacie

app = Flask(__name__)
app.secret_key = 'Wariacie, nigdy nie zgadniesz jaki jest sekretny klucz tej aplikacji'

# Sesie
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def hello():
    session["username"] = None
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    check_password = request.form['check-password']

    try:
        if password != check_password:
            flash("Hasła nie są takie same wariacie")
            return redirect('/')
        else:
            dbUsers.makeUser(username, str(generate_password_hash(password)))
            flash("Stworzono użytkownika :)")
            return redirect('/')
    except:
        flash("Podana nazwa już istnieje, sprubój coś dodać ;)")
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    
    if dbUsers.returnOneUser(username) == None:
        flash("Zły login")
        return redirect('/')
    elif not check_password_hash(dbUsers.returnOneUser(username)[2], password):
        flash("Złe hasło")
        return redirect('/')
    else:
        session["username"] = username
        return redirect('/base')
    
@app.route('/base', methods=['GET', 'POST'])
def base():
    if request.method == 'GET':
        users = dbUsers.returnUsers()
        return render_template("base.html", users=users, username=session["username"])
    else:
        try:
            user = request.form['user']
            session["user_to"] = user
        except:
            user = session["user_to"]

        users = dbUsers.returnUsers()

        messages = dbMessages.getUserMessages(session["username"], user)

        return render_template("base2.html", users=users, user=user, messages=messages, username=session["username"])

@app.route("/addMesage", methods=["POST"])
def addMesage():
    user_from = session["username"]
    user_to = request.form["user-to"]
    message = request.form['message']
    dbMessages.addMessage(user_from, user_to, message)
    return redirect("/base", code=307)



if __name__ == "__main__":
    app.run(debug=True)
