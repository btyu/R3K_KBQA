from flask import Flask, render_template, request, jsonify, send_from_directory, abort, make_response
from query_management import *
import json


app = Flask(__name__)
manager = QueryManager()


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def predict():
    query_note = None
    query_note_json = None
    text = None

    try:
        received_json = request.get_json()
        text = received_json['text']
        query_note = manager.ask(text)
    except:
        query_note = {'success': False,
                      'question': text if text is not None else '',
                      'result': '',
                      'reply': '抱歉，我的服务器出现了某些错误，请稍后重试。', }
    finally:
        query_note_json = json.dumps(query_note)
        return jsonify(query_note=query_note_json)


if __name__ == "__main__":
    app.run()
