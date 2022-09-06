from nis import match
from django.shortcuts import render
from .models import User, Match
from backend.serializer import UserSerializer, PasswordSerializer, MatchSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.

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
            return Response({
                "username": user.username, 
                "elo": user.elo
            })
        except User.DoesNotExist:
            return Response( {"status": "failed", "reason": "User doesnot exist"} )



class MatchView(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=["post"])
    def add(self, request, pk=None):
        username = request.data["username"]

        try:
            queried_user = User.objects.get(username=username)
            new_match = Match(host=queried_user)

            print(queried_user.in_game)

            if queried_user.in_game:
                return Response( {"status": "failed", "reason": "User is already in a game"} )

            if "color" not in request.data:
                new_match.white_player = queried_user
            elif request.data["color"] == "black":
                new_match.black_player = queried_user
            else:
                new_match.white_player = queried_user
            new_match.fen = "ppppkppp/pppppppp/8/8/8/8/PPPPPPPP/PPPPKPPP w - - 0 1"
            new_match.status = Match.Status.WAITING
            new_match.save()

            queried_user.in_game = new_match
            queried_user.save()

            return Response( {"status": "ok"} )

        except User.DoesNotExist:
            return Response( {"status": "failed", "reason": "User doesnot exist"} )
