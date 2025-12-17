from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .llm import chain, decoded_schema, db

views = Blueprint('views', __name__)

@views.route('/home')
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("home.html")

@views.route('/chat')
def chat():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("chat.html")

@views.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get("message") 
    if not user_message:
        return jsonify({"response": "Pergunta vazia"})

    prompt_vars = {
        "database": decoded_schema,
        "pergunta": user_message
    }

    sqlQuery = chain.invoke(prompt_vars)
    try:
        result = db.run(sqlQuery) 
        if not result:
            response_text = "Nenhum resultado encontrado."
        else:
            # Converter resposta em tabela
            headers = result[0].keys()
            rows = [list(r.values()) for r in result]
            table = "\t".join(headers) + "\n"
            for row in rows:
                table += "\t".join(str(v) for v in row) + "\n"
            response_text = table
    except Exception as e:
        response_text = f"Erro ao executar a query: {str(e)}\nQuery gerada: {sqlQuery}"

    return jsonify({'response': result + sqlQuery})
