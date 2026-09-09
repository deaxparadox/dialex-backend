from django.contrib import admin

from .models import CofounderGeneratedImage, CofounderSession, CofounderTurn

admin.site.register(CofounderSession)
admin.site.register(CofounderTurn)
admin.site.register(CofounderGeneratedImage)
