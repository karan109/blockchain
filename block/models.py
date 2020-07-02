from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Header(models.Model):
    block_number = models.IntegerField()
    previous_hash = models.CharField(max_length=64)
    nonce = models.IntegerField()
    difficulty = models.IntegerField(validators = [MaxValueValidator(6), MinValueValidator(1)], default = 2)

class Body(models.Model):
    content = models.TextField(default = 'a')


class Block(models.Model):
    header = models.ForeignKey(Header, on_delete = models.CASCADE)
    body = models.ForeignKey(Body, on_delete = models.CASCADE)

class Content(models.Model):
    content = models.TextField()