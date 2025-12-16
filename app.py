from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

WORLD_TIME_API = "http://worldtimeapi.org/api/timezone/America/Sao_Paulo"

@app.get("/")
def home():
    return jsonify({"message": "API de validação de horário funcionando!"})

@app.get("/validar-horario-bem")
def validar_horario():
    try:
        response = requests.get(WORLD_TIME_API, timeout=5)
        data = response.json()

        now_str = data.get("datetime")
        if not now_str:
            return jsonify({"error": "Não foi possível obter horário"}), 500

        now = datetime.fromisoformat(now_str)
        atual = now.hour * 60 + now.minute

        inicio = 8 * 60
        fim = 18 * 60

        valido = inicio <= atual <= fim

        return jsonify({
            "horario_atual": now.strftime("%H:%M:%S"),
            "valido": valido,
            "mensagem": "Dentro do horário permitido" if valido else "Fora do horário permitido"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
