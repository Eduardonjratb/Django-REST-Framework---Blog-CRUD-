import os
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Postt, Commen

User = get_user_model()

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postt
        fields = [
            "title",
            "description",
            "body",
            "image"
        ]

    def validate_title(self, value):
        if len(value) > 100:
            return serializers.ValidationError("El titulo acepta un maximo de 100 caracteres")
        return value

    def validate_description(self, value):
        if len(value) > 200:
            return serializers.ValidationError(
                "La descripción acepta un maximo de 200 caracteres"
            )
        return value
    
    def clean_image(self, value):
        initial_path = value.path
        new_path = settings.MEDIA_ROOT + value.name
        os.rename(initial_path, new_path)
        return value


class PostListSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Postt
        fields = [
            "id",
            "slug",
            "title",
            "author",
            "image",
            "description",
            "comments",
        ]

    def get_comments(self, obj):
        qs = Commen.objects.filter(parent=obj).count()
        return qs

    def get_slug(self, obj):
        return obj.slug


class PostDetailSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Postt
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "body",
            "author",
            "image",
            "created_at",
            "updated_at",
            "comments",
        ]

    def get_slug(self, obj):
        return obj.slug

    def get_comments(self, obj):
        qs = Commen.objects.filter(parent=obj)
        try:
            serializer = CommentSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commen
        fields = [
            "id",
            "parent",
            "author",
            "body",
            "created_at",
            "updated_at",
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commen
        fields = [
            "body",
        ]
