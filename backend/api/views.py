from nis import match
from django.shortcuts import render
from .models import User, Match
from backend.serializer import UserSerializer, PasswordSerializer, MatchSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.


# Socket views
def move(request, match_id):
    return render(request, 'move.html', {
        'match_id': match_id
    })



# Model views

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=["post"])
    def authenticate(self, request, pk=None):
        username = request.data["username"]
        password = request.data["password"]

        try:
            queried_user = self.queryset.get(username=username)
            if queried_user.check_password(password):
                return Response( {"username": username} )
            return Response( {"status": "failed", "reason": "Wrong password"} )
        except User.DoesNotExist:
            return Response( {"status": "failed", "reason": "User doesnot exist"} )

    @action(detail=False, methods=["get"])
    def getinfo(self, request, pk=None):
        try:
            user = self.queryset.get(username=request.query_params["username"])
            in_game = None if not user.in_game else user.in_game.id
            return Response({
                "username": user.username, 
                "number_of_matches": user.number_of_matches,
                "in_game": in_game,
                "elo": user.elo
            })
        except User.DoesNotExist:
            return Response( {"status": "failed", "reason": "User doesnot exist"} )

    @action(detail=False, methods=["get"])
    def getrank(self, request, pk=None):

        players = self.queryset.order_by("-elo", "number_of_matches")
        if "top" in request.query_params:
            players = players[:int(request.query_params["top"])]
        
        serializer = self.serializer_class(players, many=True, context={'request': request})

        return Response(serializer.data)



class MatchView(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=["post"])
    def add(self, request, pk=None):
        username = request.data["username"]

        try:
            queried_user = User.objects.get(username=username)
            new_match = Match(host=queried_user)

            if queried_user.in_game:
                return Response( {"status": "failed", "reason": "User is already in a game"} )

            new_match.white_player = queried_user
            new_match.white_points = 7
            new_match.fen = "ppppkppp/pppppppp/8/8/8/8/PPPPPPPP/PPPPKPPP w - - 0 1"
            new_match.status = Match.Status.WAITING
            new_match.save()

            queried_user.in_game = new_match
            queried_user.save()

            return Response( {"status": "ok"} )

        except User.DoesNotExist:
            return Response( {"status": "failed", "reason": "User doesnot exist"} )


    @action(detail=False, methods=["post"])
    def join(self, request, pk=None):
        username = request.data["username"]
        password = request.data["password"]

        try:
            queried_user = User.objects.get(username=username)
            if not queried_user.check_password(password):
                return Response( {"status": "failed", "reason": "Wrong password"} )
        except User.DoesNotExist:
            return Response( {"status": "failed", "reason": "User doesnot exist"} )

        match_id = int(request.data["match_id"])
        try:
            queried_user = User.objects.get(username=username)
            queried_match = Match.objects.get(id=match_id)
            if queried_match.black_player is not None:
                return Response( {"status": "failed", "reason": "Match is full"} )
            queried_match.black_player = queried_user
            queried_match.black_points = 6
            queried_user.in_game = queried_match
            queried_match.status = Match.Status.ONGOING
            queried_match.save()
            queried_user.save()
            return Response( {"status": "ok"} )
        except Match.DoesNotExist:
            return Response( {"status": "failed", "reason": "Match doesnot exist"} )


    @action(detail=False, methods=["post"])
    def resign(self, request, pk=None):
        username = request.data["username"]
        password = request.data["password"]

        try:
            queried_user = User.objects.get(username=username)
            if not queried_user.check_password(password):
                return Response( {"status": "failed", "reason": "Wrong password"} )
        except User.DoesNotExist:
            return Response( {"status": "failed", "reason": "User doesnot exist"} )

        match_id = int(request.data["match_id"])
        try:
            queried_user = User.objects.get(username=username)
            queried_match = Match.objects.get(id=match_id)
            queried_match.white_player.in_game = None
            queried_match.white_player.save()
            if queried_match.black_player is not None:
                queried_match.black_player.in_game = None
                queried_match.black_player.save()
            if queried_user.username == queried_match.white_player:
                queried_match.status = Match.Status.BLACK
            else:
                queried_match.status = Match.Status.WHITE
            queried_match.save()
            return Response( {"status": "ok"} )
        except Match.DoesNotExist:
            return Response( {"status": "failed", "reason": "Match doesnot exist"} )
