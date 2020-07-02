from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .models import *
from hashlib import sha256
from random import randint
nonce_max = 2**32-1

@api_view(['GET'])
def block_list(request):
	if request.method == 'GET':
		blocks = Block.objects.all().order_by()
		serializer = BlockSerializer(blocks, many=True)
		return Response(serializer.data)

@api_view(['GET', 'POST'])
def add_content(request):
	if request.method == 'POST':
		Content(content=request.data['content']).save()
		return Response(None)
	elif request.method == 'GET':
		# Content.objects.filter(id=3).delete()
		contents = Content.objects.all().order_by()
		serializer = ContentSerializer(contents, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def mine(request):
	if request.method == 'GET':
		if not Content.objects.count():
			return Response('Nothing to mine')
		body = Body(content=Content.objects.latest('id').content)
		prevblock = Block.objects.latest('id')
		previous_hash = sha256(JSONRenderer().render(BlockSerializer(prevblock).data)).hexdigest()
		block_number = prevblock.header.block_number+1
		prev_difficulty = prevblock.header.difficulty
		header = Header(block_number=block_number, previous_hash=previous_hash, nonce=None, difficulty=2)
		target = ''
		for i in range(prev_difficulty):
			target += '0'
		for i in range(64-prev_difficulty):
			target += 'f'
		while True:
			nonce = randint(0, nonce_max)
			header.nonce = nonce
			block = Block(header=header, body=body)
			block_hash = sha256(JSONRenderer().render(BlockSerializer(block).data)).hexdigest()
			if(block_hash<=target):
				break
		return Response(f'Nonce: {nonce}')

@api_view(['POST'])
def add_block(request):
	if not Content.objects.count():
		return Response('Nothing to add')
	nonce = request.data['nonce']
	prevblock = Block.objects.latest('id')
	previous_hash = sha256(JSONRenderer().render(BlockSerializer(prevblock).data)).hexdigest()
	block_number = prevblock.header.block_number+1
	prev_difficulty = prevblock.header.difficulty
	target = ''
	for i in range(prev_difficulty):
		target += '0'
	for i in range(64-prev_difficulty):
		target += 'f'
	header = Header(block_number=block_number, previous_hash=previous_hash, nonce=nonce, difficulty=2)
	body = Body(content=Content.objects.latest('id').content)
	block = Block(header=header, body=body)
	block_hash = sha256(JSONRenderer().render(BlockSerializer(block).data)).hexdigest()
	if(block_hash<=target):
		header.save()
		body.save()
		block.save()
		Content.objects.filter(id=Content.objects.latest('id').id).delete()
		return Response(BlockSerializer(block).data)
	else:
		return Response(f'Nonce {nonce} not valid')