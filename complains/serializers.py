from rest_framework import serializers
from .models import Complain, Reply, Category, ComplainAttachment, ReplyAttachment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ComplainAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplainAttachment
        fields = ['id', 'file', 'uploaded_at']

class ComplainSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.ListField(write_only=True, child=serializers.IntegerField())
    attachments = ComplainAttachmentSerializer(many=True, read_only=True)  # Show attachments
    files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )  # Accept multiple files on create

    class Meta:
        model = Complain
        fields = ['id', 'user', 'title', 'categories', 'category_ids', 'body', 'attachments', 'files', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        files = validated_data.pop('files', [])
        
        complain = Complain.objects.create(**validated_data)
        complain.categories.set(Category.objects.filter(id__in=category_ids))
        
        # Save multiple attachments
        for file in files:
            ComplainAttachment.objects.create(complain=complain, file=file)

        return complain

class ReplyAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyAttachment
        fields = ['id', 'file', 'uploaded_at']

class ReplySerializer(serializers.ModelSerializer):
    attachments = ReplyAttachmentSerializer(many=True, read_only=True)  # Show attachments
    files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )  # Accept multiple files on create

    class Meta:
        model = Reply
        fields = ['id', 'complain', 'staff', 'message', 'attachments', 'files', 'created_at']
        read_only_fields = ['staff', 'created_at']

    def create(self, validated_data):
        files = validated_data.pop('files', [])
        
        reply = Reply.objects.create(**validated_data)
        
        # Save multiple attachments
        for file in files:
            ReplyAttachment.objects.create(reply=reply, file=file)

        return reply