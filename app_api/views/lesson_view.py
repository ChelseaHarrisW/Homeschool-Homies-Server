"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models import Lesson, Parent, SkillType, Student
from rest_framework.decorators import action
# TODO IN fixtures put something in the join for attendees for seed data


class LessonView(ViewSet):
    """Lesson View"""

    def retrieve(self, request, pk):
        """Handle GET requests for single lesson
        Returns:
            Response -- JSON serialized lesson
        """

        try:
            lesson = Lesson.objects.get(pk=pk)
            #get single db lessons using the pk(id)
            parent= Parent.objects.get(user= request.auth.user)
            lesson.joined=False 
            for child in parent.children.all():
                #checking to see if the child is in the event to toggle to true
                if child in lesson.attendees.all():
                    
                    lesson.joined =True 
            serializer = LessonSerializer(lesson)
            #serialize them
            return Response(serializer.data)
        #return parsed data
        except Lesson.DoesNotExist as ex:
            #if the lesson DNE
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)#Return 404 error

    def list(self, request):
        """Handle GET requests to get all lessons
        Returns:
            Response -- JSON serialized list of lessons
        """
        lessons = Lesson.objects.all()
        #get all lessons from the DB

        lesson = request.query_params.get('lesson', None) 
        teacherlesson = request.query_params.get('teacher', None) 
        #search the param on the URL for lesson
        if lesson is not None: 
            #if there is a lesson
            lessons = lessons.filter(subject_id=lesson)
            #filter the lesson by the subject
        if lesson is not None: 
            #if there is a lesson
            teacher=teacher.get(pk=teacherlesson)
            lessons = lessons.filter(parent_id=teacher)
            #filter the lesson by the subject

        # TODO check to see if I joined property to get the attendees property on my lessons correctly
        for lesson in lessons:#iterating through lessons
            # Check to see if the student is in the attendees list on the lesson
            parent = Parent.objects.get(user=request.auth.user) 
            #student s defined as the loggedin user
        serializer = LessonSerializer(lessons, many=True) 
        #parse the data
        return Response(serializer.data) 
    #return the responds
    
    

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized lesson instance
        """
        #create will provide an Id an id for the lesson
        parent = Parent.objects.get(user=request.auth.user)
        # parent being defined as the logged-in user(which must be a parent)
        subject = SkillType.objects.get(pk=request.data['subject_id'])
        #subject is defined as the Skill type  that is located in the data
        lesson = Lesson.objects.create( 
            #create method is constructing the obj that we desire to create. think of this a key value pairs
            title=request.data["title"],
            details=request.data["details"],
            subject=subject,
            location=request.data["location"],
            min_age=request.data["min_age"],
            max_age=request.data["max_age"],
            date=request.data["date"],
            time=request.data["time"],
            parent=parent
        )
            #making sure the lesson field is valid
        serializer = LessonSerializer(lesson)
            #parse the data
        return Response(serializer.data)
        #return the responds

    def update(self, request, pk):
        """Handle PUT requests for a lesson
        Returns:
            Response -- Empty body with 204 status code
        """

        lesson = Lesson.objects.get(pk=pk)
        #get specific lesson based on primary key for the edit
        subject = SkillType.objects.get(pk=request.data['subject_id'])
        parent = Parent.objects.get(user=request.auth.user)

        lesson.title=request.data["title"]
        lesson.details=request.data["details"]
        lesson.subject=subject
        lesson.location=request.data["location"]
        lesson.min_age=request.data["min_age"]
        lesson.max_age=request.data["max_age"]
        lesson.date=request.data["date"]
        lesson.time=request.data["time"]
        lesson.parent=parent
          
        #parent is the logged in user
        # update the parent field
          
        lesson.save()
            #save re adds the lesson into the DB
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        lesson = Lesson.objects.get(pk=pk) #get the lesson based on the id
        lesson.delete() #delete method to delete the lesson
        return Response(None, status=status.HTTP_204_NO_CONTENT)#return the empty responds

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an lesson"""

        students = Student.objects.filter(parent__user=request.auth.user)
        lesson = Lesson.objects.get(pk=pk)
        lesson.attendees.add(*students)
        return Response({'message': 'Student added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete Request for a user to leave an lesson"""

        students = Student.objects.filter(parent__user=request.auth.user)
        lesson = Lesson.objects.get(pk=pk)
        lesson.attendees.remove(*students)
        return Response({'message': 'Student removed'}, status=status.HTTP_204_NO_CONTENT)


class LessonSerializer(serializers.ModelSerializer):
    """JSON serializer for lesson types
    """
    class Meta:
        model = Lesson
        fields = ('id', 'parent', 'title','details','subject', 'date', 'location',
                  "time", 'attendees', 'min_age', 'max_age', 'joined')
        depth = 2
        # depth gives all nested user data
