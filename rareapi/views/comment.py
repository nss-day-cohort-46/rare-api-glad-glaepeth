from rareapi.models.rare_users import RareUser
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, Post
from django.contrib.auth.models import User


class CommentView(ViewSet):

    # Get a single record
    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            # categories = Category.objects.filter(categorygame__)

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)


    # Get a list of all records
    def list(self, request):
        comments = Comment.objects.all()


        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)


    # Create a record
    def create(self, request):
        """Handle POST operations for comments

        Returns:
            Response -- JSON serialized event instance
        """
        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]

        post = Post.objects.get(pk=request.data["postId"])
        comment.post = post
        
        author = RareUser.objects.get(user = request.auth.user)
        comment.author = author
        
        

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    # Edit a record via PUT method
    def update(self, request, pk=None):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        # gamer = Gamer.objects.get(user=request.auth.user)
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        comment.created_on = request.data["created_on"]

        post = Post.objects.get(pk=request.data["postId"])
        comment.post = post
        author = RareUser.objects.get(user = request.auth.user)
        comment.author = author

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    # DELETE a single record 
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            user = Comment.objects.get(pk=pk)
            user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CommentSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'created_on', 'author')
        depth = 1