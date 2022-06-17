"""View module for handling requests about badge types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import BadgeType


class BadgeTypeView(ViewSet):
    """Level up badge types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single badge type
        Returns:
            Response -- JSON serialized badge type
        """
        badge_type = BadgeType.objects.get(pk=pk)
        serializer = BadgeTypeSerializer(badge_type)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all badge types
        Returns:
            Response -- JSON serialized list of badge types
        """
        # try:
        badge_type = BadgeType.objects.all()
        serializer = BadgeTypeSerializer(badge_type, many=True)
        return Response(serializer.data)
        # except BadgeType.DoesNotExist as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class BadgeTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for badge types
    """
    class Meta:
        model = BadgeType
        fields = ('id', 'label')