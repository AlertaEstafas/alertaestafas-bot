from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").lower().strip()
    num_media = int(request.values.get("NumMedia", 0))

    resp = MessagingResponse()
    msg = resp.message()

    # 🟣 Si envían imagen
    if num_media > 0:
        msg.body(
            "📸 Recibí una imagen.\n\n"
            "Por ahora no puedo analizar imágenes.\n\n"
            "⚠️ *Si tenés dudas, no avances ni compartas información personal.*"
        )
        return str(resp)

    # 🟢 Saludos / ayuda
    saludos = ["hola", "buenas", "hello", "hi"]
    ayuda = ["ayuda", "como funciona", "qué es", "que es", "info"]

    if any(palabra in incoming_msg for palabra in saludos + ayuda):
        msg.body(
            "👋 Hola! Soy AlertaEstafas\n\n"
            "Te ayudo a detectar si un mensaje puede ser una estafa.\n\n"
            "📩 Reenviame cualquier mensaje sospechoso (texto o link) y lo analizo.\n\n"
            "Cuando quieras, mandamelo 👇"
        )
        return str(resp)

    # 🟡 Intención de enviar mensaje
    continuar = ["ok", "dale", "bien", "listo", "ahí va", "ahi va", "te mando", "te paso", "ahora", "voy"]

    if any(palabra in incoming_msg for palabra in continuar):
        msg.body(
            "Perfecto 👍\n\n"
            "📩 Reenviá el mensaje sospechoso y lo analizo al instante."
        )
        return str(resp)

    # 🟢 Mensajes de cierre / agradecimiento
    cierre = ["gracias", "muy bueno", "genial", "perfecto", "me sirvio", "me sirvió", "excelente"]

    if any(palabra in incoming_msg for palabra in cierre):
        msg.body(
            "🙌 Me alegro de haberte ayudado\n\n"
            "📩 Si querés, podés enviarme otro mensaje sospechoso y lo analizo."
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
