from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from battleship import Battleship
import sys
app = Flask(__name__)
game = Battleship()


@app.route("/", methods=['POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    # Start our TwiML response
    resp = MessagingResponse()
    # Determine the right reply for this message
    try:
        resp.message(game.turn(request.values.get('From'), body))
    except:
        resp.message('Please specify coordinates in format <A-J, 1-10>.')
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, host=sys.argv[1], port=sys.argv[2])
