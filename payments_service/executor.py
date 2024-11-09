import httpx
import asyncio
from time import sleep
class executor:
    #prod
    #basepoint = 'http://broker:1446'
    #dev
    basepoint = 'http://localhost:1446'
    endpoints = {
        "messages": basepoint + "/messages",
        "queues": basepoint + "/queues"
    }

    async def make_request(self, payload, endpoint):
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, json=payload)
            return response.json()
    def verify_queue(self,queue):
        while True:
            queues = self.list_queues()
            if [x for x in queues.get("queues") if x.get("name") == queue] == []:
                print("Queue not found",flush=True)
                sleep(1)
                self.add_queue(queue)
                continue
            break

    def add_message(self, message, queue) -> dict:
        payload = {
            "action": "add_message",
            "message": message,
            "queue": queue
        }
        return asyncio.run(self.make_request(payload, self.endpoints["messages"]))

    def answer_message(self, queue, answer, id) -> dict:
        payload = {
            "action": "answer_message",
            "queue": queue,
            "answer": answer,
            "id": id
        }
        return asyncio.run(self.make_request(payload, self.endpoints["messages"]))

    def get_next_message(self, queue) -> dict:
        payload = {
            "action": "get_next_message",
            "queue": queue
        }
        return asyncio.run(self.make_request(payload, self.endpoints["messages"]))

    def get_answered_message(self, queue, id) -> dict:
        payload = {
            "action": "get_answered_message",
            "queue": queue,
            "id": id
        }
        return asyncio.run(self.make_request(payload, self.endpoints["messages"]))

    def change_message_state(self, queue, id) -> dict:
        payload = {
            "action": "change_message_state",
            "queue": queue,
            "id": id
        }
        return asyncio.run(self.make_request(payload, self.endpoints["messages"]))

    def add_queue(self, name) -> dict:
        payload = {
            "action": "add_queue",
            "name": name
        }
        return asyncio.run(self.make_request(payload, self.endpoints["queues"]))

    def list_queues(self) -> dict:
        payload = {
            "action": "list_queues"
        }
        return asyncio.run(self.make_request(payload, self.endpoints["queues"]))

    def get_queue(self, name) -> dict:
        payload = {
            "action": "get_queue",
            "name": name
        }
        return asyncio.run(self.make_request(payload, self.endpoints["queues"]))

    def remove_queue(self, name) -> dict:
        payload = {
            "action": "remove_queue",
            "name": name
        }
        return asyncio.run(self.make_request(payload, self.endpoints["queues"]))

    def __init__(self, basepoint=None):
        if basepoint:
            self.basepoint = basepoint
        self.test_executor()

    def test_executor(self) -> dict:
        try:
            response = asyncio.run(self.make_request({"test": "test"}, self.basepoint))
            return response
        except httpx.ConnectError:
            print("Broker not found, verify if the broker is working and the basepoint is correct")
            return {"status": "error", "message": "Broker not found, verify if the broker is working and the basepoint is correct"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


