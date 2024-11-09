
import executor
import json
from utils.ml_controler import ML
import os
from pathlib import Path
import requests

urlAPI = "http://localhost:4000"
    

    
if __name__ == "__main__":
    #prod
    queue = "payments_queue"
    with executor.executor() as executor_instance:
        while True:
            executor_instance.verify_queue(queue)
            message = executor_instance.get_next_message(queue)
            if message.get("status")=="empty":
                print("Empty queue",flush=True)
                continue
            print(f"Message received: {message}",flush=True)
            access_token = message['message']['message']['access_token']
            target = message['message']['message']['target']
            id = message.get("message").get("id")
            user_id = message['message']['message']['user_id']
            if target == "receive_message":
                data = None
                pass

            if not data:
                executor_instance.answer_message(queue, {"status":"no data"}, id)
            else:
                executor_instance.answer_message(queue, data, id)