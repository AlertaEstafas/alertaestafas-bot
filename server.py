from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")

    resp = MessagingResponse()
    msg = resp.message()

    sospechoso = ["premio", "ganaste", "urgente", "transferencia", "clave", "banco", "link"]

    riesgo = "🟢 Bajo riesgo"

    for palabra in sospechoso:
        if palabra in incoming_msg.lower():
            riesgo = "🔴 Posible estafa"
            break

    msg.body(f"Se analizó tu mensaje y el resultado es:\n\n*{riesgo.upper()}*\n\n⚠️ Recomendación: *Si tenés dudas, no hagas clic en enlaces ni compartas datos personales.*")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
