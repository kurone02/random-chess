import json
from channels.generic.websocket import AsyncWebsocketConsumer
from random_chess_api.gacha_chess import GachaChess, chess
from .models import Match


class JoinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = 'join_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['player']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'player': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['player']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'player': message
        }))



class MoveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        move = text_data_json['move']

        game = GachaChess(text_data_json['fen'])
        game.move(chess.Move(chess.parse_square(move["from"]), chess.parse_square(move["to"])).uci())

        print(self.room_name)
        match = Match.objects.get(id=int(self.room_name))
        match.fen = game.board.fen()
        match.save()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'move': move,
                'fen': match.fen
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        move = event['move']

        game = GachaChess(event['fen'])
        game.move(chess.Move(chess.parse_square(move["from"]), chess.parse_square(move["to"])).uci())

        # Send move to WebSocket
        await self.send(text_data=json.dumps({
            'move': move,
            'fen': game.board.fen()
        }))



class ResignConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = 'resign_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['player']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'player': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['player']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'player': message
        }))