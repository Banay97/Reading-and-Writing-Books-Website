from django.contrib import admin
from .models import User, Book, BookClub, Comment, Post, Event, Notification
# Register your models here.

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookClub)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Event)
admin.site.register(Notification)

