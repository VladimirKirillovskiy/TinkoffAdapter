from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        content = {
            'message': 'Hello, authorized user!',
            'username': request.user.username,
        }
        return Response(content)


class HelloEveryView(APIView):
    permission_classes = [AllowAny,]

    def get(self, request):
        content = {'message': 'Hello, anybody!'}
        return Response(content)
