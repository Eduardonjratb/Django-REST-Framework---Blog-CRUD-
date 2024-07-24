from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .pagination import PostLimitOffsetPagination
from .models import Postt, Commen
from .permissions import IsOwnerOrReadOnly, IsOwner
from .mixins import MultipleFieldLookupMixin
from .serializers import (
    PostCreateUpdateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentCreateUpdateSerializer,
)

# Create your views here.
class CreatePostAPIView(APIView):
    queryset = Postt.objects.all()
    serializer_class = PostCreateUpdateSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class UpdatePostAPIView(UpdateAPIView):
    queryset = Postt.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

class DeletePostAPIView(DestroyAPIView):
    queryset = Postt.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

class ListPostAPIView(ListAPIView):
    queryset = Postt.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostLimitOffsetPagination


class DetailPostAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Postt.objects.all()
    lookup_field = "slug"
    serializer_class = PostDetailSerializer


class CreateCommentAPIView(APIView):
    serializer_class = CommentCreateUpdateSerializer

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Postt, slug=slug)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ListCommentAPIView(APIView):
    def get(self, request, slug):
        post = Postt.objects.get(slug=slug)
        comments = Commen.objects.filter(parent=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class DetailCommentAPIView(MultipleFieldLookupMixin, RetrieveUpdateDestroyAPIView):
    queryset = Commen.objects.all()
    lookup_fields = ["parent", "id"]
    serializer_class = CommentCreateUpdateSerializer


class UpdateCommentAPIView(UpdateAPIView):
    queryset = Commen.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

class DeleteCommentAPIView(DestroyAPIView):
    queryset = Commen.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'