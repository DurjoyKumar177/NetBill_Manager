from django.contrib import admin
from .models import Complain, ComplainAttachment, Reply, ReplyAttachment, Category

class ComplainAttachmentInline(admin.TabularInline):
    model = ComplainAttachment
    extra = 1

class ReplyAttachmentInline(admin.TabularInline):
    model = ReplyAttachment
    extra = 1

@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    inlines = [ComplainAttachmentInline]

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('complain', 'staff', 'created_at')
    inlines = [ReplyAttachmentInline]

admin.site.register(Category)
