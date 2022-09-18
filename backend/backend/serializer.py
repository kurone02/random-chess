from api.models import User, Match
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'in_game', 'number_of_matches', 'elo', 'is_staff']

class PasswordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = ['url', 'id', 'host', 'white_player', 'white_points', 'white_pocket', 'black_player', 'black_points', 'black_pocket', 'fen', 'status']