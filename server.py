from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").lower().strip()

    resp = MessagingResponse()
    msg = resp.message()

    # 🟢 Mensajes de saludo o ayuda
    saludos = ["hola", "buenas", "hello", "hi"]
    ayuda = ["ayuda", "como funciona", "qué es", "que es", "info"]

    if any(palabra in incoming_msg for palabra in saludos + ayuda):
        msg.body(
            "👋 Hola! Soy AlertaEstafas\n\n"
            "Te ayudo a detectar si un mensaje puede ser una estafa.\n\n"
            "📩 ¿Qué podés hacer?\n"
            "Reenviame cualquier mensaje sospechoso (texto, link, etc.) y lo analizo.\n\n"
            "Ejemplo:\n"
            "'Ganaste un premio, hacé clic acá...'\n\n"
            "Y te digo si es seguro o peligroso."
        )
        return str(resp)

    # 🔴 Análisis de estafa
    sospechoso = ["premio", "ganaste", "urgente", "transferencia", "clave", "banco", "link"]

    riesgo = "🟢 Bajo riesgo"

    for palabra in sospechoso:
        if palabra in incoming_msg:
            riesgo = "🔴 Posible estafa"
            break

    msg.body(
        f"Se analizó tu mensaje y el resultado es:\n\n"
        f"*{riesgo.upper()}*\n\n"
        f"⚠️ Recomendación: *Si tenés dudas, no hagas clic en enlaces ni compartas datos personales.*"
    )

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
