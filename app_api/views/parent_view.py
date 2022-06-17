"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Parent


class ParentView(ViewSet):
    """app parent view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single parent type
        Returns:
            Response -- JSON serialized parent type
        """
        try:
            parent = Parent.objects.get(pk=pk)
            serializer = ParentSerializer(parent)
            return Response(serializer.data)
        except Parent.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all parent types
        Returns:
            Response -- JSON serialized list of parent types
        """
        parents = Parent.objects.all()

        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for parents
    """
    class Meta:
        model = Parent
        fields = ('fist_name', 'last_name', 'email')
        depth = 2
class ParentSerializer(serializers.ModelSerializer):
    """JSON serializer for parents
    """
    class Meta:
        model = Parent
        fields = ('id', 'bio', 'employment_status', 'user', 'lessons')
        depth = 2
