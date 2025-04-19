from django.contrib import admin
from .models import Game
# Register your models here.
from django.contrib import admin
from .models import Game
from .forms import GameAdminForm

class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm

admin.site.register(Game, GameAdmin)

