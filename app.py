from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

WORLD_TIME_API = "https://worldtimeapi.org/api/timezone/America/Sao_Paulo"

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

        # Horário atual em minutos
        atual = now.hour * 60 + now.minute

        inicio = 8 * 60      # 08:00
        fim = 18 * 60        # 18:00

        # Fora do horário → 403
        if atual < inicio:
            return jsonify({
                "horario_atual": now.strftime("%H:%M:%S"),
                "valido": False,
                "mensagem": "Fora do horário permitido (antes das 08:00)"
            }), 403

        if atual > fim:
            return jsonify({
                "horario_atual": now.strftime("%H:%M:%S"),
                "valido": False,
                "mensagem": "Fora do horário permitido (após as 18:00)"
            }), 403

        # Dentro do horário → 200
        return jsonify({
            "horario_atual": now.strftime("%H:%M:%S"),
            "valido": True,
            "mensagem": "Dentro do horário permitido"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
