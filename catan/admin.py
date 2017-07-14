from django.contrib import admin
from catan.models import *

# Register your models here.
admin.site.register(Player)
admin.site.register(Tile)
admin.site.register(Edge)
admin.site.register(Vertex)