from django.http import JsonResponse
from rest_framework.response import Response
from auth_app.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BoardSerializer


def testView(request):
    return JsonResponse({'message': 'geschafft'})


class BoardsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = BoardSerializer(data=request.data)
        return Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        else:
            data = serializer.errors
        return Response(data)
