"""View module for handling requests about skill types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import SkillType


class SkillTypeView(ViewSet):
    """Level up skill types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single skill type
        Returns:
            Response -- JSON serialized skill type
        """
        skill_type = SkillType.objects.get(pk=pk)
        serializer = SkillTypeSerializer(skill_type)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all skill types
        Returns:
            Response -- JSON serialized list of skill types
        """
        # try:
        skill_type = SkillType.objects.all()
        serializer = SkillTypeSerializer(skill_type, many=True)
        return Response(serializer.data)
        # except SkillType.DoesNotExist as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class SkillTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for skill types
    """
    class Meta:
        model = SkillType
        fields = ('id', 'label')