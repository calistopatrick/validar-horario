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
            return jsonify({"error": "Não foi possível obter horário."}), 500

        now = datetime.fromisoformat(now_str)
        hora = now.hour
        minuto = now.minute

        # Verifica entre 08:00 e 18:00
        inicio = 8 * 60    # 08:00
        fim = 18 * 60     # 18:00
        atual = hora * 60 + minuto

        esta_valido = inicio <= atual <= fim

        return jsonify({
            "horario_atual": now.strftime("%H:%M:%S"),
            "valido": esta_valido,
            "mensagem": "Dentro do horário permitido" if esta_valido else "Fora do horário permitido"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Porta fixa 8080 (compatível com o domínio que você criou)
    app.run(host="0.0.0.0", port=8080)
