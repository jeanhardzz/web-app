from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados e a tabela
def init_db():
    conn = sqlite3.connect('dados.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal: exibe e insere dados
@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('dados.db')
    c = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        c.execute("INSERT INTO pessoas (nome) VALUES (?)", (nome,))
        conn.commit()

    c.execute("SELECT * FROM pessoas")
    pessoas = c.fetchall()
    conn.close()

    return render_template("index.html", pessoas=pessoas)

# Rota para deletar uma pessoa pelo ID
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = sqlite3.connect('dados.db')
    c = conn.cursor()
    c.execute("DELETE FROM pessoas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

# Inicia o app e o banco
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
