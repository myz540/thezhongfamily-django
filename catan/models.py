from django.db import models


# Create your models here.
class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    victory_points = models.IntegerField()
    brick = models.IntegerField()
    wood = models.IntegerField()
    wheat = models.IntegerField()
    sheep = models.IntegerField()
    stone = models.IntegerField()
    # roads, settlements, and cities are map via foreign keys from Edge and Vertex models

    def __str__(self):
        return u"%s with %d victory points" % (self.name, self.victory_points)


class Edge(models.Model):
    id = models.IntegerField(primary_key=True)
    available = models.BooleanField(default=True)
    road = models.ForeignKey(Player, null=True)

    def __str__(self):
        return u"I am edge %d" % self.id


class Vertex(models.Model):
    id = models.IntegerField(primary_key=True)
    available = models.BooleanField(default=True)
    settlement = models.ForeignKey(Player, null=True, default=None)
    has_city = models.BooleanField(default=False)

    def __str__(self):
        return u"I am vertex %d" % self.id


class Tile(models.Model):
    id = models.IntegerField(primary_key=True)
    resource_type = models.CharField(max_length=8)
    dice_value = models.IntegerField()
    has_robber = models.BooleanField(default=False)

    # many to many relationships do not get their own column but are given a separate table
    # each tile will have 6 edges and 6 vertices, each vertex will have 1 or more tiles associated with it
    # each edge will have 1 or 2 tiles associated with it
    edge = models.ManyToManyField(Edge)
    vertex = models.ManyToManyField(Vertex)

    def __str__(self):
        return u"I am tile %d and I am a %s tile" % (self.id, self.resource_type)


class Resource(models.Model):
    brick = models.IntegerField()
    wood = models.IntegerField()
    wheat = models.IntegerField()
    sheep = models.IntegerField()
    stone = models.IntegerField()

