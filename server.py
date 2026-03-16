from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")

    resp = MessagingResponse()
    msg = resp.message()

    msg.body(f"Recibí tu mensaje: {incoming_msg}. Lo estoy analizando para detectar posibles estafas.")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
