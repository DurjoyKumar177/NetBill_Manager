from django.contrib import admin
from .models import Announcement, AnnouncementMedia, Comment, Reaction

class AnnouncementMediaInline(admin.TabularInline):
    model = AnnouncementMedia
    extra = 1

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'text', 'created_at', 'updated_at')  # Added 'title'
    list_filter = ('created_at', 'updated_at')
    search_fields = ('creator__username', 'title', 'text')  # Added 'title'
    inlines = [AnnouncementMediaInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'announcement', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'announcement__text', 'text')

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'announcement', 'reaction', 'created_at')
    list_filter = ('reaction', 'created_at')
    search_fields = ('user__username', 'announcement__text')
