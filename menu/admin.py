from django.contrib import admin

from menu.models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'parent', 'title', 'url', 'named_url')
    prepopulated_fields = {'url': ('title',)}
