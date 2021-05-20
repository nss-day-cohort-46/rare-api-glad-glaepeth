# """View module for handling requests about posts"""
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, Category, RareUser, Tag
from django.contrib.auth.models import User
from rest_framework.decorators import action

class PostView(ViewSet):
    def list(self, request):
        """Handle GET requests for posts resource

            Returns:
                Response -- JSON serialized list of posts
        """

        rare_user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.all()

        #Filter by category
        category = self.request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category__id=category)
        
        #Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            posts = posts.filter(tag__id=tag)
        
        #Filter by tag
        user = self.request.query_params.get('user', None)
        if user is not None:
            posts = posts.filter(user__id=user)


        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)
                
    
    def retrieve(self, request, pk):

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        post = Post()
        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        post.user = user
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        
        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])
        post = Post.objects.get(pk=pk)
        post.user = user
        post.category = category
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class PostUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['user', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    user = PostUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')                