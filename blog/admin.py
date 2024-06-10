from django.contrib import admin
from .models import User, Tag, Blog, Comment, Like

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Like)
