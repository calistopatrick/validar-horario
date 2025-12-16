from flask import Flask, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

app = Flask(__name__)

TIMEZONE = ZoneInfo("America/Sao_Paulo")

@app.get("/")
def home():
    return jsonify({"message": "API de validação de horário funcionando!"})

@app.get("/validar-horario-bem")
def validar_horario():
    try:
        now = datetime.now(TIMEZONE)

        atual = now.hour * 60 + now.minute
        inicio = 8 * 60     # 08:00
        fim = 18 * 60       # 18:00

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

        return jsonify({
            "horario_atual": now.strftime("%H:%M:%S"),
            "valido": True,
            "mensagem": "Dentro do horário permitido"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
