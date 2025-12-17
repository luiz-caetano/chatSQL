from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
import os
import mysql.connector
from dotenv import load_dotenv 
load_dotenv()



db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        senha = request.form["senha"]
        
        cursor.execute("SELECT * FROM usuario_site WHERE username = %s", (username,))
        usuario = cursor.fetchone()
        
        if usuario and current_app.bcrypt.check_password_hash(usuario["Senha"], senha):
            session["user_id"] = usuario["Username"]
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("views.chat"))
        else:
            flash("Usuário ou senha incorretos.", "danger")
            return redirect(url_for("auth.login"))
        
    return render_template("login.html")


@auth.route('/logout')
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("auth.login"))