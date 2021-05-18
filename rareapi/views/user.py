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


   
    # def create(self, request):
    #     """Handle POST operations

    #     Returns:
    #         Response -- JSON serialized game instance
    #     """

    #     # Uses the token passed in the `Authorization` header
    #     gamer = Gamer.objects.get(user=request.auth.user)

        
    #     game = RareUser()
    #     game.ages = request.data["ages"]
    #     game.description = request.data["description"]
    #     game.est_time = request.data["est_time"]
    #     game.maker = request.data["maker"]
    #     game.number_of_players = request.data["number_of_players"]
    #     game.title = request.data["title"]
    #     game.year = request.data["year"]
        

    #     try:
    #         game.save()
    #         categories = Category.objects.in_bulk(request.data["categories"])
    #         game.categories.set(categories)
    #         serializer = RareUserSerializer(game, context={'request': request})
    #         return Response(serializer.data)

    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    

    # # Edit a record via PUT method
    # def update(self, request, pk=None):
    #     """Handle PUT requests for a game

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     game = RareUser.objects.get(pk=pk)
    #     game.ages = request.data["ages"]
    #     game.description = request.data["description"]
    #     game.est_time = request.data["est_time"]
    #     game.maker = request.data["maker"]
    #     game.number_of_players = request.data["number_of_players"]
    #     game.title = request.data["title"]
    #     game.year = request.data["year"]
        
    #     categories = Category.objects.in_bulk(request.data["categories"])
    #     game.categories.set(categories)

    #     game.save()
    
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)
   

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
        fields = ('first_name', 'last_name')
        

class RareUserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'active')
        depth = 1