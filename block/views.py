from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

@api_view(['GET', 'POST'])
def block_list(request):
    if request.method == 'GET':
        blocks = Block.objects.all().order_by()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # handle
        return Response(None)