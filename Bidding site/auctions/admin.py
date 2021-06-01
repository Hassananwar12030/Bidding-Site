from django.contrib import admin
from . import models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ("username","email")

class ListAdmin(admin.ModelAdmin):
	list_display = ("id","title","bidPrice", "item_creator")


admin.site.register(models.User, UserAdmin)
admin.site.register(models.list_item, ListAdmin)
admin.site.register(models.bid)
admin.site.register(models.comment)
admin.site.register(models.watchlist)