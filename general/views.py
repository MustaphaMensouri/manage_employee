from .serializers import FermeSerializer
from .models import Ferme
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Create your views here.


@api_view(['GET', 'POST'])
def view_ferme(request):
    if request.method == "GET":
        data = Ferme.objects.all()
        serializer = FermeSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = FermeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "successfully created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "this is not valide"}, status=status.HTTP_400_BAD_REQUEST)
