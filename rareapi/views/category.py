from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category
from django.core.exceptions import ValidationError

class CategoryView(ViewSet):
    def create(self, request):


        category = Category()
        category.label = request.data["label"]



        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):  
        categories = Category.objects.all()


        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):

        if request.auth.user.is_staff:
            category = Category.objects.get(pk=pk)
            category.label = request.data["label"]
            category.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk=None):

        if request.auth.user.is_staff:

            try:
                category = Category.objects.get(pk=pk)
                category.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Category.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            
class CategorySerializer(serializers.ModelSerializer):
# how we build the object

    class Meta:
        model = Category
        fields = ('id', 'label')        