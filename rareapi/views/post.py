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
        
        
        #TODO: check on connecting category id
        #TODO:join tags table



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



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved')                