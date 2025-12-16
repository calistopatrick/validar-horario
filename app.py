from flask import Flask, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

app = Flask(__name__)

TIMEZONE = ZoneInfo("America/Sao_Paulo")

@app.get("/")
def home():
    return jsonify({"message": "API de validação de dia da semana funcionando!"})

@app.get("/validar-dia-semana")
def validar_dia_semana():
    try:
        now = datetime.now(TIMEZONE)

        # Monday = 0 ... Sunday = 6
        dia_semana = now.weekday()

        # ❌ Final de semana
        if dia_semana >= 5:
            return jsonify({
                "data": now.strftime("%Y-%m-%d"),
                "dia_semana": now.strftime("%A"),
                "valido": False,
                "mensagem": "Acesso não permitido (final de semana)"
            }), 403

        # ✅ Dia útil
        return jsonify({
            "data": now.strftime("%Y-%m-%d"),
            "dia_semana": now.strftime("%A"),
            "valido": True,
            "mensagem": "Acesso permitido (dia útil)"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # 🔥 IMPORTANTE: faz a API abrir no navegador
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
