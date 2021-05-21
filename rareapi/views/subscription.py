"""View module for handling requests"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Subscription
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser

class SubscriptionView(ViewSet):
    """Rare App"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized game instance
        """

        # Create a new Python instance of the Subscription class
        # and set its properties from what was sent in the
        # body of the request from the client.
        subscription = Subscription()
        subscription.follower = request.data["follower"]
        subscription.author = request.data["author"]
        subscription.created_on = request.data["created_on"]
        subscription.ended_on = request.data["ended_on"]

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            subscription.save()
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Handle GET requests for single subscription

        Returns:
            Response -- JSON serialized subscription instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/tags/2
            #
            # The `2` at the end of the route becomes `pk`
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to subscription resources

        Returns:
            Response -- JSON serialized list of subscriptions
        """
        # Get all game records from the database
        subscription = Subscription.objects.all()

        serializer = SubscriptionSerializer(
            subscription, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a subscription
        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        if request.auth.user.is_staff:
            subscription = Subscription.objects.get(pk=pk)
            subscription.follower = request.data["follower"]
            subscription.author = request.data["author"]
            subscription.created_on = request.data["created_on"]
            subscription.ended_on = request.data["ended_on"]

            subscription.save()

            # 204 status code means everything worked but the
            # server is not sending back any data in the response
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    # @permission_classes([IsAdminUser])
    def destroy(self, request, pk):
        """Handle DELETE requests for a single subscription

        Returns:
            Response -- 200, 404, or 500 status code
        """
        
        if request.auth.user.is_staff:
            try:
                subscription = Subscription.objects.get(pk=pk)
                subscription.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Subscription.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

class SubscriptionSerializer(serializers.ModelSerializer):
    """JSON serializer for subscriptions

    Arguments:
        serializer type
    """
    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'author', 'created_on', 'ended_on')
