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

        match = Match.objects.get(id=int(self.room_name))

        game = GachaChess(match.fen, white_points=match.white_points, black_points=match.black_points)
        game.move(chess.Move(chess.parse_square(move["from"]), chess.parse_square(move["to"])).uci())


        match.black_points = game.black_player.points
        match.white_points = game.white_player.points

        match.fen = game.board.fen()
        match.save()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'move': move,
                'fen': match.fen,
                'player': text_data_json['player']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        move = event['move']

        game = GachaChess(event['fen'])

        # Send move to WebSocket
        await self.send(text_data=json.dumps({
            'move': move,
            'fen': game.board.fen(),
            'player': event['player']
        }))


class RandomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = 'random_%s' % self.room_name

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
        
        match = Match.objects.get(id=int(self.room_name))

        game = GachaChess(match.fen, white_points=match.white_points, black_points=match.black_points)
        piece = game.gacha()

        if piece is None:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'status': 'failed',
                    'reason': 'not enough points',
                    'player': text_data_json["player"],
                }
            )
            return

        match.black_points = game.black_player.points
        match.white_points = game.white_player.points

        piece = chess.Piece(piece, game.current_turn()).symbol()

        if game.current_turn() == chess.WHITE:
            match.white_pocket["pocket"].append(piece)
        else:
            match.black_pocket["pocket"].append(piece)

        match.save()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'status': 'ok',
                'piece': piece,
                'player': text_data_json["player"],
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send move to WebSocket
        await self.send(text_data=json.dumps(event))



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