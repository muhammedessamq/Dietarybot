from flask import Flask, request
import sys
from pprint import pprint
from pymessenger import Bot
from Api import generate_user_response

VERIFICATION_TOKEN = "hello"
app = Flask(__name__)
PAGE_ACCESS_TOKEN = "EABM1Q1FtEcoBALfMpzu5iOhilZBcxxH3TBGxu4coE88yWulZAozydEFsbMgFC0Sg9xYyu36mblQ2ZAhCRJZCLclO8HbVgZCNq4nMNmTy3ZCov5WZBRWrsXNDxLhRIZBIlMOZBeRYquCp0IJ3xXJZBZBkyZCI1poaZB6LQXBRxyoZAyZABvXe2VugazQ09qX"
bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello-world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    printmsg(data)
    process_data(data)
    return "ok", 200

def printmsg(msg):
    pprint(msg)
    sys.stdout.flush()

def process_data(data):
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]
                if messaging_event.get("message"):
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                    else:
                        messaging_text = "no text"
                    printmsg(messaging_text)
                    response = generate_user_response(messaging_text)
                    bot.send_text_message(sender_id, response)


def send_response(sender_id,response):
    bot.send_text_message(sender_id,response)

if __name__ == '__main__':
    app.run(debug=True, port=80)



