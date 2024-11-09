import flask
import message as ms_object
import logging

app = flask.Flask(__name__)
messages_instance = ms_object.messages()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.route('/',methods=["GET","POST"])
def index():
    return {"status":"running"}

@app.route('/messages',methods=["GET","POST"])
def messages():
    _json = flask.request.json
    action = _json.get('action')
    if action == "add_message":
        _message = _json.get('message')
        _queue = _json.get('queue')
        new_message = messages_instance.add_message(_message,_queue)
        print(new_message.as_dict())
        return flask.jsonify({"message":new_message.as_dict()})
    elif action == "answer_message":
        queue = _json.get('queue')
        answer = _json.get('answer')
        id = int(_json.get('id'))
        messages_instance.answer_message(queue,answer,id)
        return flask.jsonify({"message":"answered"})
    elif action == "get_next_message":
        queue = _json.get('queue')
        message = messages_instance.get_next_message(queue)
        if not message:
            return flask.jsonify({"message":"no messages on queue","status":"empty"})
        return flask.jsonify({"message":message.as_dict(),"status":"waiting"})
    elif action == "get_answered_message":
        queue = _json.get('queue')
        id = int(_json.get('id'))
        message = messages_instance.get_answered_message(id,queue)
        return flask.jsonify({"message":message.as_dict()})
    elif action == "change_message_state":
        queue = _json.get('queue')
        id = int(_json.get('id'))
        message = messages_instance.change_message_state(id,queue)
        return flask.jsonify({"message":message.as_dict()})
    return flask.jsonify({"message":"no action"})

@app.route("/queues",methods=["GET","POST"])
def queues():
    _json = flask.request.json
    action = _json.get('action')
    if action == "add_queue":
        name = _json.get('name')
        new_queue = messages_instance.queues.add_queue(name)
        return flask.jsonify({"queue":new_queue.as_dict()})
    elif action == "list_queues":
        queues = messages_instance.queues
        return flask.jsonify(queues.as_dict())
    elif action == "get_queue":
        name = _json.get('name')
        queue = messages_instance.queues.get_queue(name)
        return flask.jsonify({"queue":queue.as_dict()})
    elif action == "remove_queue":
        name = _json.get('name')
        messages_instance.queues.remove_queue(name)
        return flask.jsonify({"message":"queue removed"})
    return flask.jsonify({"message":"no action"})




if __name__ == '__main__':
    app.run(debug=True)