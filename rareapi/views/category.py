from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category

class CategoryView(ViewSet):


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


        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, pk=None):

        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CategorySerializer(serializers.ModelSerializer):
# how we build the object

    class Meta:
        model = Category
        fields = ('id', 'label')        