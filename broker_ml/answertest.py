import executor

queue = "crawlerPR"
id = 0
executor_instance = executor.executor()

message = executor_instance.get_next_message(queue)
print(message)
queue = message["message"]["queue"]
id = message["message"]["id"]
executor_instance.answer_message(queue,"answer",id)
