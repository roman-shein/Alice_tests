from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

agree_words = ["ладно", "куплю", "покупаю", "хорошо"]


@app.route("/post", methods=["POST"])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        "session": request.json["session"],
        "version": request.json["version"],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return jsonify(response)


def handle_dialog(req, res):
    user_id = req["session"]["user_id"]

    if req["session"]["new"]:
        new_user(user_id, res)
        return

    for el in agree_words:
        if el in req["original_utterance"].lower():
            agree_user(res)
            return

    res["response"]["text"] = f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res["response"]["buttons"] = get_suggest(user_id)


def get_suggest(user_id):
    session = sessionStorage[user_id]["suggests"]
    suggests = [{"title": suggest, "hide": True} for suggest in session[:2]]
    session = session[1:]
    sessionStorage[user_id]["suggest"] = session

    if len(suggests) < 2:
        suggests.append({"title": "Ладно", "url": "https://market.yandex.ru/search?text=слон", "hide": True})
    return suggests


def new_user(user_id, res):
    sessionStorage[user_id] = {
        "suggest": ["Не буду.", "Не хочу.", "Отстань!"]
    }

    res["response"]["text"] = "Привет! Купи слона!"
    res["response"]["buttons"] = get_suggest(user_id)


def agree_user(res):
    res["response"]["text"] = "Слона можно найти на Яндекс.Маркете!"
    res["response"]["end"] = True
