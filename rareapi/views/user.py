from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import RareUser
from django.contrib.auth.models import User


class RareUserView(ViewSet):
    
    # Get a single record
    def retrieve(self, request, pk=None):
        try:
            rare_user = RareUser.objects.get(pk=pk)
            # categories = Category.objects.filter(categorygame__)
            
            serializer = RareUserSerializer(rare_user, context={'request': request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    # # Get a list of all records
    def list(self, request):
        users = RareUser.objects.all()
        

        serializer = RareUserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)
    

    # # Edit a record via PUT method
    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        # gamer = Gamer.objects.get(user=request.auth.user)
        user = RareUser.objects.get(pk=pk)
        user.bio = request.data["bio"]
        user.profile_image_url = request.data["profile_image_url"]
        user.created_on = request.data["created_on"]
        user.active = request.data["active"]
        
        user.save()
    
        return Response({}, status=status.HTTP_204_NO_CONTENT)
   

    # DELETE a single record 
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            user = RareUser.objects.get(pk=pk)
            user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_staff', 'email')
        

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)   
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'active', 'user')
        