from django.contrib import admin
from .models import Post, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "pub_date", "edit_date"]
    search_fields = ["user", "title", "pub_date", "edit_date"]
    list_filter = ["user", "pub_date", "edit_date"]
    list_display_links = ["title"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "user", "content"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
