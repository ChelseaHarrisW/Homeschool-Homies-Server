from django.db import models


class Lesson(models.Model):
    parent = models.ForeignKey("Parent", on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=50)
    details = models.CharField(max_length=50)
    subject = models.ForeignKey("SkillType", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=50)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    attendees = models.ManyToManyField("Student", related_name="lessons")
    #organizer = models.ForeignKey("Parent", on_delete=models.CASCADE)

#Dropping the _id for game because Django is compairing the intire game not just the id field

#adding the gamer info for join table as attendees. THAT IS Your join table^^

#decorators change what comes next modifies the function

    @property #this is declaring that we will be using joined
    def joined(self):
        return self.__joined
    
    @joined.setter #getter is the default so gere we are setting the property
    def joined(self, value):
        self.__joined = value