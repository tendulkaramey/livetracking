import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import asyncio
from threading import Thread


#group to broadcast message when any one in group sends  a message.
class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["name"]
        self.room_group_name = f"test_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        pass
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message = "sending now" + message

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "test.group.message", "message": message}
        )

    # Receive message from room group
    def test_group_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


#group broad cast as well as sends period message to group
class TestConsumerGroupPeriodic(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["name"]
        self.room_group_name = f"test_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        # Start sending periodic messages
        Thread(target=self.send_periodic_messages).start()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "test.group.message", "message": message}
        )

    # Receive message from room group
    def test_group_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))

    def send_periodic_messages(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.periodic_message_loop())

    async def periodic_message_loop(self):
        while True:
            await asyncio.sleep(5)
            periodic_message = "This is a periodic message to the group"
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "test.group.message", "message": periodic_message}
            )

#normal websocket 1:1 and also sends period messages.
class TestConsumerBasicAsync(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Start sending periodic messages
        self.periodic_task = asyncio.create_task(self.send_periodic_messages())

    async def disconnect(self, close_code):
        # Stop sending periodic messages when the connection is closed
        self.periodic_task.cancel()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        if message:
            # If user sends a message, send back a response
            response_message = "Received: " + message
            await self.send(text_data=json.dumps({"message": response_message}))
        else:
            # Handle periodic messages (e.g., log them)
            print("Received a periodic message from the client")


    async def send_periodic_messages(self):
        while True:
            # Send periodic messages to the client
            await self.send(text_data=json.dumps({"message": "This is a periodic message from the server"}))
            await asyncio.sleep(15)

#normal basic setup
class TestConsumerBasic(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message = "sending now" + message

        self.send(text_data=json.dumps({"message": message}))