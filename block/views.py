from django.shortcuts import render
#from django.http import HttpResponse
#from rest_framework.parsers import JSONParser
from .models import Body, Header, Content, Block
from .serializers import BodySerializer, HeaderSerializer, ContentSerializer, BlockSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from hashlib import sha256
#from random import randint
from rest_framework import status
import requests
from django.urls import reverse

hash_max = 2**256-1
#desired_diff = 
desired_diff = 8
link = 'http://localhost:8000'

@api_view(['GET', 'POST'])
def block_list(request):
    if request.method == 'GET':
        blocks = Block.objects.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            content = request.data['content']
            content_response = requests.post(link+reverse('add-content'), json = {"content": content})
            mine_response = requests.post(link+reverse('mine'), json = content_response.json())
            add_response = requests.post(link+reverse('add-block'), json = mine_response.json())
            return Response(add_response.json(), status = status.HTTP_201_CREATED)
        except:
            return Response({"error": "Content not found"}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def add_content(request):
    if request.method == 'GET':
        content = Content.objects.all().order_by('-id')
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ContentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def mine(request):
    if request.method == 'GET':
        content = Content.objects.all().order_by('-id')
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not Content.objects.count():
            return Response({'error': 'Nothing to mine'}, status = status.HTTP_400_BAD_REQUEST)
        try:
            mine_id = int(request.data['id'])
            content = Content.objects.get(id = mine_id).content
            body = Body(content=content)
            #print(body.content)
            prevblock, previous_hash, block_number = None, None, None
            try:
                prevblock = Block.objects.latest('id')
                previous_hash = sha256(JSONRenderer().render(BlockSerializer(prevblock).data)).hexdigest()
                block_number = prevblock.header.block_number+1
            except:
                previous_hash = '0'*64
                block_number = 1
            header = Header(block_number=block_number, previous_hash=previous_hash, nonce=None, difficulty=2**desired_diff)
            target = int(hash_max/(2**desired_diff))
            nonce = 0
            while True:
                header.nonce = nonce
                block = Block(header=header, body=body)
                #print(JSONRenderer().render(BlockSerializer(block).data))
                block_hash = sha256(JSONRenderer().render(BlockSerializer(block).data)).hexdigest()
                block_hash_dec = int(block_hash, 16)
                if(block_hash_dec<=target):
                    return Response({'id': mine_id, 'nonce': nonce, 'hash': block_hash})
                nonce += 1
        except:
            return Response({'error': 'No such content id'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def add_block(request):
    if request.method == 'GET':
        content = Content.objects.all().order_by('-id')
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':       
        if not Content.objects.count():
            return Response({'error': 'Nothing to add'}, status = status.HTTP_400_BAD_REQUEST)
        try:
            add_id = int(request.data['id'])
            nonce = int(request.data['nonce'])
            prevblock, previous_hash, block_number = None, None, None
            try:
                prevblock = Block.objects.latest('id')
                previous_hash = sha256(JSONRenderer().render(BlockSerializer(prevblock).data)).hexdigest()
                block_number = prevblock.header.block_number+1
            except:
                previous_hash = '0'*64
                block_number = 1
            target = int(hash_max/(2**desired_diff))
            header = Header(block_number=block_number, previous_hash=previous_hash, nonce=nonce, difficulty=2**desired_diff)
            body = Body(content=Content.objects.get(id = add_id).content)
            block = Block(header=header, body=body)
            block_hash = sha256(JSONRenderer().render(BlockSerializer(block).data)).hexdigest()
            block_hash_dec = int(block_hash, 16)
            if(block_hash_dec <= target):
                header.save()
                body.save()
                block.save()
                Content.objects.filter(id = add_id).delete()
                data = BlockSerializer(block).data
                data['hash'] = block_hash
                return Response(data, status = status.HTTP_201_CREATED)
            return Response({"error": "Invalid Nonce"}, status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Invalid ID/Nonce"}, status = status.HTTP_400_BAD_REQUEST)
