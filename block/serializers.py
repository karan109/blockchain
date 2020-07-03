from .models import Block, Header, Body, Content
from rest_framework import serializers

class HeaderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Header
		fields = ('block_number', 'previous_hash', 'nonce', 'difficulty')

class BodySerializer(serializers.ModelSerializer):
	class Meta:
		model = Body
		fields = ('content',)

class ContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Content
		fields = ('id', 'content')
	
class BlockSerializer(serializers.ModelSerializer):
	header = HeaderSerializer()
	body = BodySerializer()
	class Meta:
		model = Block
		fields = ('header', 'body')
