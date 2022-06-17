"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Student


class StudentView(ViewSet):
    """app student view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single student type
        Returns:
            Response -- JSON serialized student type
        """
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all student types
        Returns:
            Response -- JSON serialized list of student types
        """
        students = Student.objects.all()

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class StudentSerializer(serializers.ModelSerializer):
    """JSON serializer for students
    """
    class Meta:
        model = Student
        fields = ('id', 'age', 'parent')
        depth = 1