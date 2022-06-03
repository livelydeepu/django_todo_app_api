from django.contrib import admin

# Register your models here.

from .models import Todo, Tag

admin.site.register(Todo)
admin.site.register(Tag)
